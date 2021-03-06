import asyncpg

import config


class PostgresClient:

    @staticmethod
    async def create():
        self = PostgresClient()
        self._db_client = await asyncpg.connect(config.DATABASE_URL)

    async def make_subscribe(self, chat_id):
        await self._db_client.execute('''
        INSERT INTO subscriptions(chat_id) VALUES ($1)
        ON CONFLICT DO NOTHING
        ''', chat_id)


async def get_client() -> PostgresClient:
    global client
    if not client:
        client = await PostgresClient.create()
    return client


client = None
