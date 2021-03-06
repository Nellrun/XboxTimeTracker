import asyncio
import datetime
from typing import NamedTuple, List

import config
import pg
import pytz

from aiogram import Bot

utc = pytz.UTC


class PlayerStats(NamedTuple):
    gamertag: str
    playtime: datetime.timedelta


def format_string(playtime: datetime.timedelta):
    playtime.total_seconds()
    hours, minutes = playtime.seconds//3600, (playtime.seconds//60)%60
    if not hours:
        return f'{minutes} minutes'
    return f'{hours}:{minutes} hours'


def format_message(player_stats: List[PlayerStats]):
    sorted_list = sorted(
        player_stats, key=lambda x: x.playtime.total_seconds(), reverse=True)

    messages = []
    for player in sorted_list:
        messages.append(f'{player.gamertag} - {format_string(player.playtime)}')

    return messages


async def main():
    bot = Bot(config.TOKEN)
    pg_client = await pg.get_client()

    chats = await pg_client.get_subscribed_chats()

    day_end = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    day_start = day_end - datetime.timedelta(days=1)

    history = await pg_client.get_history_sessions(
        day_start,
        day_end
    )

    stats_by_players = {}

    for elem in history:
        start = max(elem['start_at'], utc.localize(day_start))
        end = min(elem['ended_at'], utc.localize(day_end))

        gamertag = elem['gamertag']

        if gamertag not in stats_by_players:
            stats_by_players[gamertag] = datetime.timedelta()

        stats_by_players[gamertag] += end - start

    players_stats = []
    for key, value in stats_by_players.items():
        players_stats.append(PlayerStats(gamertag=key, playtime=value))

    message = 'Today stats:\n' + '\n'.join(format_message(players_stats))

    for chat in chats:
        await bot.send_message(int(chat['chat_id']), message)

    await pg_client.close()
    await bot.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
