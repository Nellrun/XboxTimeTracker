import asyncio
import os

import asyncpg


DATABASE_URL = os.getenv('DATABASE_URL', '')

async def main():

    conn = await asyncpg.connect(DATABASE_URL)

    await conn.execute('''
        CREATE TABLE if not exists subscriptions(
            chat_id TEXT PRIMARY KEY,
            updated  TIMESTAMPTZ DEFAULT NOW(),
            created  TIMESTAMPTZ DEFAULT NOW()
        )
    ''')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
