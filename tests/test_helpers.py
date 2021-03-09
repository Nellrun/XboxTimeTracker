import datetime

from MinecraftBot import helpers

import pytest


@pytest.mark.parametrize('seconds, expected_string', [
    (0, '0 minutes'),
    (60, '1 minutes'),
    (3600, '01:00 hours'),
    (3670, '01:01 hours'),
    (36000, '10:00 hours'),
    (36900, '10:15 hours')
])
def test_format_playtime(seconds, expected_string):
    playtime = datetime.timedelta(seconds=seconds)
    assert helpers.format_playtime(playtime) == expected_string
