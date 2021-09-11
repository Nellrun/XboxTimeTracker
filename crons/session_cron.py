import asyncio
import datetime
import pytz
from typing import Dict

import config
import postgres
import helpers
import xbox_live

from aiogram import Bot

ITERATIONS = 18
SLEEP_TIME = 30

utc = pytz.UTC


async def get_active_sessions(
        pg_client: postgres.client.PostgresClient,
) -> Dict[str, postgres.models.Session]:
    pg_sessions = await pg_client.get_active_sessions()

    sessions = {}
    for session in pg_sessions:
        sessions[session.gamertag] = session
    return sessions


async def main():
    bot = Bot(config.TOKEN)
    client = xbox_live.client.get_client()
    pg_client = await postgres.client.get_client()

    chats = await pg_client.get_subscribed_chats()

    for _ in range(ITERATIONS):
        players = await client.get_players()
        sessions = await get_active_sessions(pg_client)

        for player in players:
            if player.online:
                if player.gamertag not in sessions:
                    await pg_client.create_new_session(player.gamertag, player.game)
                    if player.game != 'Home':
                        for chat in chats:
                            await bot.send_message(int(chat.chat_id),
                                                   f'{player.gamertag} is playing {player.game}')
                else:
                    session_game = sessions[player.gamertag].game
                    if player.game != session_game:
                        session = sessions[player.gamertag]
                        await pg_client.end_session(session.id)

                        ended_at = utc.localize(datetime.datetime.utcnow())
                        session_time = ended_at - session.start_at

                        formated_time = helpers.format_playtime(session_time)

                        for chat in chats:
                            if player.game != 'Home':
                                await bot.send_message(int(chat.chat_id),
                                                       f'{player.gamertag} played {session_game} '
                                                       f'(session: {formated_time})')

        await asyncio.sleep(SLEEP_TIME)

    await client.close()
    await pg_client.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
