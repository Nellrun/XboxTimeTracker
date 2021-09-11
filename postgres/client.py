import datetime
from typing import Optional, List

import config
from postgres import models

import asyncpg


SESSION_STATUS_ACTIVE = 'active'
SESSION_STATUS_ENDED = 'ended'


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

    async def get_subscribed_chats(self) -> List[models.Subscription]:
        res = await self._db_client.fetch('''
        SELECT chat_id FROM subscriptions
        ''')

        return [models.Subscription(**subs) for subs in res]

    async def get_active_sessions(self):
        res = await self._db_client.fetch('''
        SELECT id, gamertag, game, start_at FROM sessions WHERE status = $1
        ''', SESSION_STATUS_ACTIVE)

        return [models.Session(**row) for row in res]

    async def create_new_session(self, gamertag: str, game: str):
        await self._db_client.execute('''
        INSERT INTO sessions(gamertag, game, status, start_at) VALUES ($1, $2, $3, $4)
        ''', gamertag, game, SESSION_STATUS_ACTIVE, datetime.datetime.utcnow())

    async def end_session(self, session_id):
        await self._db_client.execute('''
        UPDATE sessions
        set status = $1,
        ended_at = $2,
        updated = $2
        WHERE id = $3
        ''', SESSION_STATUS_ENDED, datetime.datetime.utcnow(), session_id)

    async def get_history_sessions(
            self, date_start: datetime.datetime,
            date_end: datetime.datetime) -> List[models.Session]:
        res = await self._db_client.fetch('''
        SELECT id, gamertag, game, start_at, ended_at
        FROM sessions
        WHERE (start_at < $1 AND ended_at >= $2)
        OR (start_at < $1 and ended_at is NULL)
        ''', date_end, date_start)

        return [models.Session(**row) for row in res]

    async def get_history_full(self) -> List[models.Session]:
        res = await self._db_client.fetch('''
        SELECT id, gamertag, game, start_at, ended_at
        FROM sessions
        ''')

        return [models.Session(**row) for row in res]

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
