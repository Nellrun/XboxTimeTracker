import config

from aiohttp import ClientSession
from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse


class XboxClient:

    _session: ClientSession
    _client: XboxLiveClient

    def __init__(self):
        _session = ClientSession()

        auth_mgr = AuthenticationManager(
            _session, config.XBOX_CLIENT_ID, config.XBOX_CLIENT_SECRET, ''
        )

        auth_mgr.oauth = OAuth2TokenResponse.parse_raw(config.XBOX_TOKEN)
        _client = XboxLiveClient(auth_mgr)

    def __del__(self):
        _session.close()


def get_client():
    global client

    if client:
        return client

    client = XboxClient()
    return client


client = XboxClient()
