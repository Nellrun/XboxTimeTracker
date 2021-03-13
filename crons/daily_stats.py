import asyncio
import datetime
import pytz

import config
import postgres
import helpers

from aiogram import Bot
from aiogram.types import ParseMode

utc = pytz.UTC


async def main():
    bot = Bot(config.TOKEN)
    pg_client = await postgres.client.get_client()

    chats = await pg_client.get_subscribed_chats()

    day_end = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    day_start = day_end - datetime.timedelta(days=1)

    history = await pg_client.get_history_sessions(
        day_start,
        day_end
    )

    stats_by_players = {}

    for elem in history:
        start = max(elem.start_at, utc.localize(day_start))
        end = utc.localize(day_end)
        if elem.ended_at:
            end = min(elem.ended_at, utc.localize(day_end))

        gamertag = elem.gamertag

        if gamertag not in stats_by_players:
            stats_by_players[gamertag] = datetime.timedelta()

        stats_by_players[gamertag] += end - start

    players_stats = []
    for key, value in stats_by_players.items():
        players_stats.append(helpers.Playtime(gamertag=key, playtime=value))

    today_str = datetime.date.today().strftime('%d/%m/%Y')

    message = f'*Today stats {today_str}:*\n' + '\n'.join(
        helpers.format_playtime_message(players_stats),
    )

    for chat in chats:
        await bot.send_message(
            int(chat.chat_id), message, parse_mode=ParseMode.MARKDOWN
        )

    await pg_client.close()
    await bot.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
