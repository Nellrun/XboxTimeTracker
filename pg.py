from typing import Optional

import config

import asyncpg


class PostgresClient:
    _db_client = None

    @staticmethod
    async def create():
        self = PostgresClient()
        self._db_client = await asyncpg.connect(config.DATABASE_URL)
        return self

    async def make_subscribe(self, chat_id: str):
        await self._db_client.execute('''
        INSERT INTO subscriptions(chat_id) VALUES ($1)
        ON CONFLICT DO NOTHING
        ''', str(chat_id))

    async def close(self):
        await self._db_client.close()


async def get_client() -> PostgresClient:
    global client
    if not client:
        client = await PostgresClient.create()
    return client


async def close():
    if client:
        await client.close()

client: Optional[PostgresClient] = None
