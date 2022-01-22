from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Tuple
from dataclasses import dataclass
import orjson
from ...utils import resolve_dict_path

if TYPE_CHECKING:
    from ...hypixel import Hypixel

@dataclass
class SkyHelperCredentials:
    """A dataclass meant to contain SkyHelper API information"""
    instance: str
    key: str
    port: int = 3000

@dataclass
class FetchurItem:
    """A dataclass containing a fetchur item"""
    name: str
    quantity: int
    text: str
    image: str

class SkyHelperWrapper:
    """A Wrapper for the SkyHelper API: https://github.com/Altpapier/SkyHelperAPI

    hypy will automatically instantiate this class at Hypixel.skyhelper if an instance of SkyHelperCredentials gets passed into it during construction.
    """

    def __init__(self, hypixel: Hypixel, creds: SkyHelperCredentials):
        self.hypixel = hypixel
        self.creds = creds

    async def _get(self, route) -> Tuple[int, Dict]:
        url = f'{self.creds.instance}:{self.creds.port}/v1'
        async with self.hypixel.session.get(f'{url}{route}', headers={'Authorization': self.creds.key}) as res:
            jsn = await res.json(loads=orjson.loads)
            return res.status, jsn

    async def get_fetchur_item(self) -> FetchurItem:
        """Gets the current Fetchur item from the SkyHelper API"""
        data = (await self._get('/fetchur'))[1]['data']
        return FetchurItem(data['name'], data['quantity'], data['text'], data["image"])

    async def get_profile(self, nameOrUuid: str, profile: str = None, auto_find_path: str = "last_save") -> dict:
        """Get Information regarding a player from the SkyHelper API

        :param nameOrUuid: The name or uuid of the player
        :param profile: Optionally, the cute_name of a profile
        :param auto_find_path: This will only be used if profile isnt passed. It will be passed as a sort key to automatically determine a profile.
        """
        path = f'/profiles/{nameOrUuid}'
        if profile:
            path = path.replace('/profiles/', '/profile/')
            path += f'/{profile}'
        data = (await self._get(path))[1]['data']
        if not profile:
            data = sorted(data, key=lambda x: resolve_dict_path(x, auto_find_path))[-1] # I'm not a huge fan of this approach, but it gets the job done.
        return data

    async def get_networth(self, nameOrUuid: str, profile: str = None):
        """A more specialized variant of get_profile, get networth information from the SkyHelper API

        :param nameOrUuid: The name or uuid of the player
        :param profile: Optionally, the cute_name of a profile
        """
        return (await self.get_profile(nameOrUuid, profile, 'networth.total_networth'))['networth']
