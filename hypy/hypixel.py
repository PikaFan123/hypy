from typing import Tuple, Optional
import asyncio
import traceback
from time import time_ns as timestamp
from asyncio import sleep
from urllib.parse import quote
from orjson import orjson
import aiohttp
from .player import Player
from .mojang import Mojang
from .playerstatus import PlayerStatus
from .exceptions import (
    ContentTypeException,
    MissingParamException,
    HypixelNoSuccess,
    ExceededMaxRetries,
    InvalidAccountDescriptor,
    NotEnoughArguments,
)
from .guild import Guild
from .hypixelresources import SkyBlockResources
from .auctions import SkyblockAuctions
from .auction import multi_init
from . import utils
from .utils import Utils
from .models import KeyStats, WatchdogStats
from .profile import SkyblockProfile
from .bazaar import Bazaar
from .hypixelfriends import HypixelFriends
from .playercounts import PlayerCounts
from .ext.skyhelper import SkyHelperWrapper, SkyHelperCredentials


class Hypixel:
    """The main object used to interact with the Hypixel API

    Before interacting with the api you need to call Hypixel.setup()
    """

    _apikey = ""
    loop: asyncio.AbstractEventLoop
    session: aiohttp.ClientSession
    _base_url = "https://api.hypixel.net/"
    mojang: Mojang
    _sb_resources = None
    utils = None
    _debug = False
    __version__ = "1.4.0"
    _retry = False
    _max_retries = 0
    _total_calls = 0
    skyhelper: Optional[SkyHelperWrapper] = None

    def __init__(
        self,
        key,
        *,
        session: aiohttp.ClientSession = None,
        debug: bool = False,
        retry: bool = False,
        max_retries: int = 5,
        loop: asyncio.AbstractEventLoop = None,
        skyhelper_credentials: SkyHelperCredentials = None
    ):
        if session is not None:
            self.session = session
        self._apikey = key
        self._debug = debug
        self._retry = retry
        self._max_retries = max_retries
        self._headers = {"API-Key": self._apikey}
        self.loop = loop or asyncio.get_event_loop()
        if skyhelper_credentials:
            self.skyhelper = SkyHelperWrapper(self, skyhelper_credentials)


    async def close(self) -> None:
        """Close internal session"""
        await self.session.close()

    async def setup(self) -> None:
        """Properly set up Hypixel object"""
        if not hasattr(self, "session"):
            self.session = aiohttp.ClientSession(loop=self.loop)
        self.mojang = Mojang(session=self.session)
        self._sb_resources = await self.update_resources()
        self.utils = Utils(self._sb_resources)

    def _debug_url(self, endpoint, **params) -> str:
        """Generate a debug url for endpoint and parameters"""
        url = f"{self._base_url}{endpoint}?key={self._apikey}"
        for key, value in params.items():
            if key == "_HYPY_RETRIES":
                continue
            url += f"&{key}={quote(value)}"
        return url

    async def _get(self, endpoint, **params) -> Tuple[int, dict]:
        """GET something from the Hypixel API"""
        self._total_calls += 1
        endpoint = endpoint.lstrip("/")  # is this even needed
        if self._debug:
            print(self._debug_url(endpoint, **params))
        url = f"{self._base_url}{endpoint}?"
        retries = 0
        if "_HYPY_RETRIES" in params:
            retries = int(params["_HYPY_RETRIES"])
            del params["_HYPY_RETRIES"]
        for key, value in params.items():
            url += f"{key}={quote(value)}&"
        url = url[:-1]
        async with self.session.get(url, headers=self._headers) as res:
            try:
                jsn = await res.json(loads=orjson.loads)
                if not jsn["success"]:
                    raise HypixelNoSuccess(jsn["cause"])
                return res.status, jsn
            except aiohttp.client_exceptions.ContentTypeError:
                if self._debug:
                    print("In contenttype handler")
                if not self._retry:
                    raise ContentTypeException(res.headers.get("content-type"))
                if retries > self._max_retries:
                    raise ExceededMaxRetries(self._max_retries)
                if self._debug:
                    print("RETRYING {} RETRY NUMBER {}".format(url, retries + 1))
                rrq = await self._get(
                    endpoint, **dict(**params, **{"_HYPY_RETRIES": retries + 1})
                )
                return rrq[0], rrq[1]
            except aiohttp.ClientResponseError:
                if self._debug:
                    traceback.print_exc()
                raise

    async def get_player(self, nameOrUuid: str) -> Player:
        """Returns a Player object for a given name or UUID

        :param nameOrUuid: The name or uuid of the player
        """
        if utils.is_username(nameOrUuid):
            nameOrUuid = await self.mojang.name_to_uuid(nameOrUuid)
        elif not utils.is_uuid(nameOrUuid):
            raise InvalidAccountDescriptor(nameOrUuid)

        _, response = await self._get("/player", uuid=nameOrUuid)
        return Player(response, nameOrUuid, self)

    async def get_player_status(self, nameOrUuid: str) -> PlayerStatus:
        """Returns status of player

        :param nameOrUuid: The name or uuid of the player
        """
        if utils.is_username(nameOrUuid):
            nameOrUuid = await self.mojang.name_to_uuid(nameOrUuid)
        elif not utils.is_uuid(nameOrUuid):
            raise InvalidAccountDescriptor(nameOrUuid)

        _, response = await self._get("/status", uuid=nameOrUuid)
        return PlayerStatus(response)

    async def get_guild(
        self, name: str = None, guild_id: str = None, playerNameOrUuid: str = None
    ) -> Optional[Guild]:
        """Gets a guild based on one of three parameters

        :param name: The name of a guild
        :param guild_id: The id of a guild
        :param playerNameOrUuid: The name or uuid of a guild member
        """
        if name is not None:
            _, response = await self._get("/guild", name=name)
        elif guild_id is not None:
            _, response = await self._get("/guild", id=guild_id)
        elif playerNameOrUuid is not None:
            if utils.is_username(playerNameOrUuid):
                playerNameOrUuid = await self.mojang.name_to_uuid(playerNameOrUuid)
            elif not utils.is_uuid(playerNameOrUuid):
                raise InvalidAccountDescriptor(playerNameOrUuid)
            _, response = await self._get("/guild", player=playerNameOrUuid)
        else:
            raise NotEnoughArguments("name, id, playerNameOrUuid")

        if response["guild"] is not None:
            return Guild(response, self)
        return None

    async def get_key_stats(self) -> KeyStats:
        """Gets statistics of API Key"""
        _, res = await self._get("/key")
        res = res["record"]
        return KeyStats(
            res["owner"],
            await self.mojang.uuid_to_name(res["owner"]),
            res["totalQueries"],
            res["queriesInPastMin"],
            timestamp(),
        )

    async def get_watchdog_stats(self) -> WatchdogStats:
        """Gets punishment statistics"""
        _, res = await self._get("punishmentstats")
        return WatchdogStats(
            res["watchdog_lastMinute"],
            res["staff_rollingDaily"],
            res["watchdog_total"],
            res["watchdog_rollingDaily"],
            res["staff_total"],
        )

    async def get_profile(self, profile_id: str, uuid: str) -> SkyblockProfile:
        """Gets a Hypixel SkyBlock Profile

        For general usage, going through :py:func:`hypy.player.Player.find_profile` is better

        :param profile_id: The id of the profile
        :param uuid: The uuid of the player
        """
        if not profile_id:
            raise MissingParamException("name, profile_id")
        _, raw_profile_data = await self._get("skyblock/profile", profile=profile_id)

        return SkyblockProfile(raw_profile_data, uuid, self)

    async def get_profile_data(self, profile_id) -> dict:
        """Gets Hypixel SkyBlock Profile data based on profile id"""
        if not profile_id:
            raise MissingParamException("name, profile_id")
        _, raw_profile_data = await self._get("skyblock/profile", profile=profile_id)

        return raw_profile_data

    async def get_friends(self, nameOrUuid: str) -> HypixelFriends:
        """Gets Friends of given name or UUID

        Args:
            nameOrUuid: The name or uuid of the player
        """
        if utils.is_username(nameOrUuid):
            nameOrUuid = await self.mojang.name_to_uuid(nameOrUuid)
        elif not utils.is_uuid(nameOrUuid):
            raise InvalidAccountDescriptor(nameOrUuid)

        _, response = await self._get("/friends", uuid=nameOrUuid)
        return HypixelFriends(response, self)

    async def get_auctions(self) -> SkyblockAuctions:
        """Gets Hypixel SkyBlock auctions"""
        all_itime_equal = False
        while not all_itime_equal:
            _, init_response = await self._get("/skyblock/auctions")
            i_time = init_response["lastUpdated"]
            i_pages = init_response["totalPages"]
            results = [
                x[1]
                for x in list(
                    await asyncio.gather(
                        *[
                            self._get("skyblock/auctions", page=str(pn))
                            for pn in range(1, i_pages)
                        ]
                    )
                )
            ]
            results.insert(0, init_response)
            all_itime_equal = all([i_time == x["lastUpdated"] for x in results])
            if not all_itime_equal:
                await sleep(10)  # i think this is good to do regardless
        return SkyblockAuctions(
            *await asyncio.to_thread(multi_init, results, self), self
        )

    async def find_guild(self, nameOrUuid) -> Optional[Guild]:
        """Deprecated, use Hypixel.getGuild instead"""
        return await self.get_guild(playerNameOrUuid=nameOrUuid)

    async def get_bazaar(self) -> Bazaar:
        """Gets bazaar information"""
        _, response = await self._get("/skyblock/bazaar")
        return Bazaar(response)

    async def get_player_counts(self) -> PlayerCounts:
        """Get Hypixel Player counts"""
        _, response = await self._get("/counts")
        return PlayerCounts(response)

    async def update_resources(self) -> SkyBlockResources:
        """Update Hypixel Resources"""
        _, response = await self._get("/resources/skyblock/skills")
        self._sb_resources = SkyBlockResources(response)
        return self._sb_resources # this makes mypy happy
