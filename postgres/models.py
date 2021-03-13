import datetime
from typing import Optional, NamedTuple


class Session(NamedTuple):
    id: int
    gamertag: str
    start_at: datetime.datetime
    ended_at: Optional[datetime.datetime] = None


class Subscription(NamedTuple):
    chat_id: str
