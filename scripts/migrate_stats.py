import argparse
import asyncio
import csv
import datetime
import typing

import asyncpg


START_DATE = datetime.datetime(2000, 1, 1)
SESSION_STATUS_ENDED = 'ended'
DATABASE_URL = ''

def fetch_stat(file_path: str) -> typing.Dict[str, int]:
    result = {}
    with open(file_path) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        for row in reader:
            result[row['\ufeff"Игра"']] = int(row['Минут в игре'])
        return result


async def worker(args):
    stat = fetch_stat(args.path)

    conn = await asyncpg.connect(DATABASE_URL)
    for game, time in stat.items():
        if time <= 0:
            continue
        print(game, time)
        await conn.execute('''
        INSERT INTO sessions(gamertag, game, game_detailed, status, start_at, ended_at) VALUES ($1, $2, $3, $4, $5, $6)
        ''', args.gamertag, game, game, SESSION_STATUS_ENDED, START_DATE, START_DATE + datetime.timedelta(minutes=time))


def main():
    parser = argparse.ArgumentParser(description="migrate xbox stats")
    parser.add_argument(
        '--path',
        required=True,
        help='path to csv file',
    )
    parser.add_argument(
        '--gamertag',
        required=True,
        help='nickname of player',
    )
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker(args))


if __name__ == "__main__":
    main()