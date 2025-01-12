from typing import List

import config
from xbox_live import models

from aiohttp import ClientSession
from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse


XBOX_STATE_ONLINE = 'Online'


class XboxClient:

    _session: ClientSession
    _client: XboxLiveClient

    def __init__(self):
        self._session = ClientSession()

        auth_mgr = AuthenticationManager(
            self._session, config.XBOX_CLIENT_ID, config.XBOX_CLIENT_SECRET, ''
        )

        auth_mgr.oauth = OAuth2TokenResponse.parse_raw(config.XBOX_TOKEN)
        self._client = XboxLiveClient(auth_mgr)

    async def get_online(self) -> List[models.PlayerInfo]:
        players = await self.get_players()

        online = []

        for player in players:
            if player.online:
                online.append(player)

        return online

    async def get_players(self) -> List[models.PlayerInfo]:
        def format_game(presence_text: str, rich_precense: str):
            if rich_precense:
                return presence_text.split(rich_precense)[0].split('-')[0].strip()
            return presence_text

        players = []
        friends = await self._client.people.get_friends_own()

        for friend in friends.people:
            presence_details = None
            for detail in friend.presence_details:
                if detail.presence_text == friend.presence_text:
                    presence_details = detail
                    break

            if presence_details:
                game = format_game(friend.presence_text, presence_details.rich_presence_text)
            else:
                game = friend.presence_text

            players.append(
                models.PlayerInfo(
                    gamertag=friend.modern_gamertag,
                    online=friend.presence_state == XBOX_STATE_ONLINE,
                    game=game,
                    game_detailed=friend.presence_text
                )
            )

        return sorted(players, key=lambda x: x.game)

    async def close(self):
        await self._session.close()


def get_client():
    global client

    if not client:
        client = XboxClient()

    return client


async def close():
    if client:
        await client.close()


client = XboxClient()
