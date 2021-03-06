from typing import List

import config

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
    

    async def get_minecraft_online(self) -> List[str]:
        online = []

        me = await self._client.presence.get_presence_own()
        if me.state == XBOX_STATE_ONLINE:
            online.append('Nellrun')

        friends = await self._client.people.get_friends_own()

        
        for friend in friends.people:
            if friend.presence_state == XBOX_STATE_ONLINE:
                if friend.presence_text.find('Minecraft') >= 0:
                    online.append(friend.modern_gamertag)
        
        return online


    def __del__(self):
        self._session.close()


def get_client():
    global client

    if not client:
        client = XboxClient()

    return client


client = XboxClient()
