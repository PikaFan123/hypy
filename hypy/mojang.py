from typing import Tuple, List, Optional
from datetime import datetime
import aiohttp
from orjson import orjson
from .exceptions import UUIDNotFound, UsernameNotFound, InvalidHTTPCode

class NameHistoryEntry:
    """An Entry in a players name history"""
    changed_to_at: Optional[datetime] = None
    name: str = ""
    uuid: str = ""

    def __init__(self, raw, uuid):
        self.uuid = uuid
        if 'changedToAt' in raw:
            self.changed_to_at = datetime.utcfromtimestamp(raw['changedToAt'] / 1000)
        self.name = raw['name']

    def __str__(self):
        return f'<hypy.NameHistoryEntry uuid={self.uuid} name={self.name} changed_to_at={self.changed_to_at}>'

class Mojang:
    """A simple wrapper for Mojangs API

    If you are using this with hypy, the Hypixel class already has an instance of this class ready, you do not need to instantiate it yourself
    """

    session: aiohttp.ClientSession
    _base_url = "https://api.mojang.com/"

    def __init__(self, *, session: aiohttp.ClientSession = None) -> None:
        self.session = session or aiohttp.ClientSession()

    async def _get(self, endpoint, base_url="https://api.mojang.com/") -> Tuple[int, dict]:
        endpoint = endpoint.lstrip("/")  # is this even needed
        url = f"{base_url}{endpoint}"
        async with self.session.get(url) as res:
            return res.status, await res.json(loads=orjson.loads)

    async def close(self) -> None:
        """Close internal aiohttp session"""
        await self.session.close()

    async def name_to_uuid(self, name) -> str:
        """Returns UUID for given name

        :param name: The name of the player
        """
        status, response = await self._get(f"/users/profiles/minecraft/{name}")
        if status == 200:
            return response["id"]
        elif status == 204:
            raise UsernameNotFound(name)
        return ""

    async def uuid_to_name(self, uuid) -> str:
        """Returns name for given UUID

        :param uuid: The uuid of the player
        """
        status, response = await self._get(f'session/minecraft/profile/{uuid}', 'https://sessionserver.mojang.com/')
        if status == 200:
            return response["name"]
        elif status == 400:
            raise UUIDNotFound(uuid)
        return ""
