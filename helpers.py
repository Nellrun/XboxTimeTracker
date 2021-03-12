import datetime
import collections
from typing import List, NamedTuple

from MinecraftBot.pg import Session

import pytz


class Playtime(NamedTuple):
    gamertag: str
    playtime: datetime.timedelta


def format_playtime(playtime: datetime.timedelta):
    total_seconds = int(playtime.total_seconds())

    hours = total_seconds // 3600
    minutes = (total_seconds // 60) % 60

    if not hours:
        return f'{minutes} minutes'
    return '{:02}:{:02} hours'.format(hours, minutes)


def calc_total_time_by_gametag(sessions: List[Session]) -> List[Playtime]:
    """
    returns dict gamertag - timedelta
    """
    now = datetime.datetime.now(tz=pytz.utc)
    result = collections.defaultdict(datetime.timedelta)
    for session in sessions:
        start = session.start_at
        end = session.ended_at or now

        result[session.gamertag] += end - start

    return [
        Playtime(gamertag, playtime) for gamertag, playtime in result.items()
    ]


def format_playtime_message(time_by_player: List[Playtime]) -> List[str]:
    sorted_list = sorted(
        time_by_player, key=lambda x: x.playtime.total_seconds(), reverse=True)

    lines = []
    for player in sorted_list:
        lines.append(f'{player.gamertag} - {format_playtime(player.playtime)}')
    return lines
