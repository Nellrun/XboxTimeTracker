import asyncio

import config

import asyncpg


async def main():
    conn = await asyncpg.connect(config.DATABASE_URL)

    await conn.execute('''
        CREATE TABLE if not exists subscriptions(
            chat_id TEXT PRIMARY KEY,
            updated  TIMESTAMPTZ DEFAULT NOW(),
            created  TIMESTAMPTZ DEFAULT NOW()
        )
    ''')

    await conn.execute('''
        CREATE TABLE if not exists sessions(
            id SERIAL PRIMARY KEY,
            gamertag TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            start_at  TIMESTAMPTZ DEFAULT NOW(),
            ended_at  TIMESTAMPTZ DEFAULT NULL,
            updated  TIMESTAMPTZ DEFAULT NOW()
        )
    ''')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
