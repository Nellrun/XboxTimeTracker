import asyncio
import datetime
import pytz
from typing import NamedTuple, Dict

import config
import pg
import helpers
import xbox_client

from aiogram import Bot

ITERATIONS = 9
SLEEP_TIME = 60

utc = pytz.UTC

class Session(NamedTuple):
    gamertag: str
    id: str
    start_at: datetime.datetime


async def get_active_sessions(pg_client: pg.PostgresClient) -> Dict[str, Session]:
    pg_sessions = await pg_client.get_active_sessions()

    sessions = {}
    for session in pg_sessions:
        sessions[session['gamertag']] = Session(gamertag=session['gamertag'],
                                                id=session['id'],
                                                start_at=session['start_at'])
    return sessions


async def main():
    bot = Bot(config.TOKEN)
    client = xbox_client.get_client()
    pg_client = await pg.get_client()

    chats = await pg_client.get_subscribed_chats()

    for _ in range(ITERATIONS):
        players = await client.get_players()
        sessions = await get_active_sessions(pg_client)

        for player in players:
            if player.online and player.game.find('Minecraft') >= 0:
                if player.gamertag not in sessions:
                    await pg_client.create_new_session(player.gamertag)
                    for chat in chats:
                        await bot.send_message(int(chat['chat_id']),
                                               f'{player.gamertag} is now online')
            if not player.online:
                if player.gamertag in sessions:
                    session = sessions[player.gamertag]
                    await pg_client.end_session(session.id)

                    session_time = utc.localize(datetime.datetime.utcnow()) - \
                                   session.start_at

                    formated_time = helpers.format_playtime(session_time)

                    for chat in chats:
                        await bot.send_message(int(chat['chat_id']),
                                               f'{player.gamertag} is now '
                                               f'offline (session: {formated_time})')

        await asyncio.sleep(SLEEP_TIME)

    await client.close()
    await pg_client.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
