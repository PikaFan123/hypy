from typing import Tuple
import aiohttp
from orjson import orjson
from .exceptions import UUIDNotFound, UsernameNotFound


class Mojang:
    """A simple wrapper for Mojangs API

    If you are using this with hypy, the Hypixel class already has an instance of this class ready, you do not need to instantiate it yourself
    """

    _session: aiohttp.ClientSession
    _base_url = "https://api.mojang.com/"

    def __init__(self, *, session: aiohttp.ClientSession = None) -> None:
        self._session = session or aiohttp.ClientSession()

    async def _get(self, endpoint) -> Tuple[int, dict]:
        endpoint = endpoint.lstrip("/")  # is this even needed
        url = f"{self._base_url}{endpoint}"
        async with self._session.get(url) as res:
            return res.status, await res.json(loads=orjson.loads)

    async def close(self) -> None:
        """Close internal aiohttp session"""
        await self._session.close()

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
        status, response = await self._get(f"/user/profiles/{uuid}/names")
        if status == 200:
            return response[-1]["name"]
            # response[-1]['name']
        elif status == 204:
            raise UUIDNotFound(uuid)
        return ""
