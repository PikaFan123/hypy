from typing import Callable, Optional, List, Tuple
from datetime import datetime
from .exceptions import (
    MissingParamException,
    InvalidProfileNameException,
    InvalidProfileException,
    NoProfileInfoAvailableException,
    NoProfilesFoundException,
)
from .profile import SkyblockProfile
from .vars import skills, types, cute_names
from .hypyobject import HypyObject
from .socialmedia import SocialMedia
from .hypixelplayer import HypixelPlayer


class Player(HypyObject, HypixelPlayer):
    """A Hypixel Player"""

    __slots__ = ("_raw", "_hypy", "_uuid")

    displayname: str
    """The display name of the player"""

    def __init__(self, data, uuid, hypy) -> None:
        self._hypy = hypy
        self._uuid = self.uuid = uuid
        self._raw = data = data["player"]
        if "displayname" in data:
            self.displayname = data["displayname"]
        else:
            self.displayname = data["playername"]

    def __repr__(self) -> str:
        return f"<hypy.Player {self.displayname} last_login={self.last_login}>"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def first_login(self) -> datetime:
        """The first login of the Player"""
        return datetime.utcfromtimestamp(self._raw["firstLogin"] / 1000)

    @property
    def last_login(self) -> datetime:
        """The last login of the Player"""
        return datetime.utcfromtimestamp(self._raw["lastLogin"] / 1000)

    @property
    def last_logout(self) -> datetime:
        """The last logout of the Player"""
        return datetime.utcfromtimestamp(self._raw["lastLogout"] / 1000)

    @property
    def social_media(self) -> SocialMedia:
        """The players social media information"""
        return SocialMedia(self._raw)

    @property
    def achievement_skills(self) -> dict:
        """SkyBlock skill data from achievements"""
        rt: dict = {"detail": {}, "avg": 0}
        for skill in skills:
            qdic = self._raw["achievements"]
            qstr = f"skyblock_{types[skill]}"
            if qstr not in qdic:
                rt["detail"][skill] = 0
                continue
            if skill in ["catacombs"]:
                rt["detail"][skill] = qdic[qstr]
            else:
                lvl = qdic[qstr]
                rt["detail"][skill] = lvl
                rt["avg"] += lvl
        rt["avg"] /= 8
        return rt

    @property
    def skyblock_profiles(self) -> List[dict]:
        """SkyBlock Profiles of the Player"""
        plist = []
        for _, value in self._raw["stats"]["SkyBlock"]["profiles"].items():
            plist.append(value)
        return plist

    async def get_profile(self, *, name=None, profile_id=None) -> SkyblockProfile:
        """Gets a Hypixel SkyBlock Profile from name OR profile id

        :param name: The cute name (eg. Strawberry) of a profile
        :param profile_id: The profile_id of a profile
        """
        if not profile_id:
            if not name:
                raise MissingParamException("name, profile_id")
            if name not in cute_names:
                raise InvalidProfileNameException(name)
            pl = [
                (x["profile_id"], x["cute_name"])
                for x in self.skyblock_profiles
                if x["cute_name"] == str.capitalize(str.lower(name))
            ]
            if len(pl) == 0:
                raise InvalidProfileException(f"{name} {profile_id}")
            profile_id = pl[0][0]
            cute_name = pl[0][1]

        profile = await self._hypy.get_profile(profile_id, self._uuid)
        profile.add_cute_name(cute_name)
        return profile

    async def find_profile(
        self, *, key: Callable
    ) -> Tuple[SkyblockProfile, Optional[str]]:
        """Find Hypixel SkyBlock Profile by a metric

        :param key: The key to find the profile by, most likely a lambda (eg. find_profile(key=lambda p: p.skills.avg))
        """
        profiles = [
            await self.get_profile(name=profile["cute_name"])
            for profile in self.skyblock_profiles
        ]
        profiles = [p for p in profiles if not p.deleted]
        if len(profiles) == 0:
            raise NoProfileInfoAvailableException()
        match = sorted(profiles, key=key, reverse=True)[0]
        if match is not None:
            return match, match.cute_name
        raise NoProfilesFoundException(self._uuid)
