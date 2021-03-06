import datetime


def format_playtime(playtime: datetime.timedelta):
    playtime.total_seconds()
    hours, minutes = playtime.seconds // 3600, (playtime.seconds // 60) % 60

    if not hours:
        return f'{minutes} minutes'
    return '{:02}:{:02} hours'.format(hours, minutes)
