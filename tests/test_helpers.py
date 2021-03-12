import datetime

from MinecraftBot import helpers
from MinecraftBot.pg import Session

import pytest


def make_time(hour: int, minute: int):
    return datetime.datetime(2021, 3, 12, hour, minute)


@pytest.mark.parametrize('seconds, expected_string', [
    (0, '0 minutes'),
    (60, '1 minutes'),
    (3600, '01:00 hours'),
    (3670, '01:01 hours'),
    (36000, '10:00 hours'),
    (36900, '10:15 hours'),
    (360000, '100:00 hours')
])
def test_format_playtime(seconds, expected_string):
    playtime = datetime.timedelta(seconds=seconds)
    assert helpers.format_playtime(playtime) == expected_string


@pytest.mark.parametrize('sessions, expected', [
    ([
        Session(0, 'player1', make_time(0, 0), make_time(0, 10))
    ], [
        helpers.Playtime('player1', datetime.timedelta(minutes=10))
    ]),
    ([
         Session(0, 'player1', make_time(0, 0), make_time(0, 10)),
         Session(0, 'player2', make_time(0, 0), make_time(1, 10))
     ], [
         helpers.Playtime('player1', datetime.timedelta(minutes=10)),
         helpers.Playtime('player2', datetime.timedelta(hours=1, minutes=10))
    ]),
    ([
         Session(0, 'player1', make_time(0, 0), make_time(0, 10)),
         Session(0, 'player1', make_time(0, 0), make_time(1, 10))
     ], [
         helpers.Playtime('player1', datetime.timedelta(hours=1, minutes=20))
     ])
])
def test_calc_playtime(sessions, expected):
    result = helpers.calc_total_time_by_gametag(sessions)
    assert len(result) == len(expected)

    for elem, expected_elem in zip(result, expected):
        assert elem.gamertag == expected_elem.gamertag
        assert elem.playtime == expected_elem.playtime


@pytest.mark.parametrize('time_to_player, expected_lines', [
    ([
        helpers.Playtime('player1', datetime.timedelta(hours=10)),
        helpers.Playtime('player2', datetime.timedelta(days=1)),
    ], [
        'player2 - 24:00 hours', 'player1 - 10:00 hours'
    ]),
    ([
         helpers.Playtime('player1', datetime.timedelta(minutes=10)),
     ], [
         'player1 - 10 minutes'
     ])
])
def test_format_playtime_message(time_to_player, expected_lines):
    result = helpers.format_playtime_message(time_to_player)
    assert len(result) == len(expected_lines)
    for res_line, expected_line in zip(result, expected_lines):
        assert res_line == expected_line
