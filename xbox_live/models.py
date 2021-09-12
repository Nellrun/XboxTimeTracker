from typing import NamedTuple


class PlayerInfo(NamedTuple):
    gamertag: str
    online: bool
    game: str
    game_detailed: str
