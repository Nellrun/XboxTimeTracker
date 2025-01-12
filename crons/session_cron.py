import asyncio
import datetime
import random
import pytz
from typing import Dict

import config
import postgres
import helpers
import xbox_live
from utils.logger import logger

from aiogram import Bot

ITERATIONS = 18
SLEEP_TIME = 50

utc = pytz.UTC

BANNED_GAMES = {
    "Home",
    "Xbox App"
}


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
    while True:
        try:
            random_value = random.randint(0, 50)
            logger.info(f'random is {random_value}')
            if random_value == 25:
                logger.info('updating client')
                await client.close()
                client = xbox_live.client.get_client()
            logger.info('getting chats')
            chats = await pg_client.get_subscribed_chats()

            logger.info('getting friends and sessions')
            players = await client.get_players()
            logger.info(f'found players {players}')

            sessions = await get_active_sessions(pg_client)
            logger.info(f'found active sessions {sessions}')

            for player in players:
                if player.online:
                    if player.gamertag not in sessions:
                        logger.info(f'open new session for player {player.gamertag} with game {player.game} ({player.game_detailed})')
                        await pg_client.create_new_session(player.gamertag, player.game, player.game_detailed)
                        # if player.game not in BANNED_GAMES:
                        #     for chat in chats:
                        #         await bot.send_message(int(chat.chat_id),
                        #                                f'{player.gamertag} is playing {player.game}')
                if player.gamertag in sessions:
                    session = sessions[player.gamertag]
                    if player.game_detailed != session.game_detailed:
                        session = sessions[player.gamertag]
                        logger.info(f'closing session for player {player.gamertag}')
                        await pg_client.end_session(session.id)

                        ended_at = utc.localize(datetime.datetime.utcnow())
                        session_time = ended_at - session.start_at

                        formated_time = helpers.format_playtime(session_time)

                        for chat in chats:
                            if session.game not in BANNED_GAMES:
                                await bot.send_message(int(chat.chat_id),
                                                       f'{player.gamertag} played {session.game} '
                                                       f'(session: {formated_time})')
        except Exception as exc:
            print(exc)
        sleep_time = SLEEP_TIME + random.randint(0, 20)
        logger.info(f'going to sleep for {sleep_time} sec')
        await asyncio.sleep(sleep_time)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
