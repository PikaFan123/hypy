import datetime as dt
import asyncio
from typing import Iterator, List
from .exceptions import NotInGuildException
from .uuid import UUID
from .player import Player
from .hypyobject import HypyObject
from .abc import HypyIterable
from .guildrank import GuildRank
from .guildmember import GuildMember


class Guild(HypyObject, HypyIterable):
    """A Hypixel Guild"""

    __slots__ = (
        "_raw",
        "_hypy",
        "_id",
    )

    name: str
    """The name of the guild"""
    members: List[GuildMember]
    """A list of GuildMembers"""

    def __init__(self, data: dict, hypy) -> None:
        self._hypy = hypy
        self._raw: dict = data["guild"]
        self.name = self._raw["name"]
        self.members: List[GuildMember] = [
            GuildMember(x, self, hypy) for x in self._raw["members"]
        ]
        self._id = self._raw["_id"]

    def __len__(self) -> int:
        return len(self.members)

    def __iter__(self) -> Iterator[GuildMember]:
        for i in self.members:
            yield i

    def iter_uuids(self) -> Iterator[UUID]:
        for i in self.members:
            yield UUID(i["uuid"])

    @property
    def uuid_list(self) -> List[str]:
        """List of UUIDs of players in guild"""
        li = []
        for mem in self._raw["members"]:
            li.append(UUID(mem["uuid"]).no_dashes)
        return li

    async def name_list(self) -> List[str]:
        """Get list of names of players in guild"""
        return await asyncio.gather(
            *[self._hypy.mojang.uuid_to_name(uuid) for uuid in self.uuid_list]
        )

    async def player_list(self) -> List[Player]:
        """Get list of hypy.Player objects for players in guild"""
        return await asyncio.gather(
            *[self._hypy.get_player(uuid) for uuid in self.uuid_list]
        )

    def when_joined(self, uuid) -> dict:
        """Check when a player joined the guild

        :param uuid: The uuid of the player
        """
        tr = {"inGuild": False, "joinedAt": dt.datetime.utcfromtimestamp(0)}
        uuid = UUID(uuid).no_dashes
        m = [x for x in self.members if x["uuid"] == uuid]
        if len(m) > 0:
            tr["inGuild"] = True
            tr["joinedAt"] = dt.datetime.utcfromtimestamp(m[0]["joined"] / 1000)
        return tr

    def rank_of(self, uuid) -> GuildRank:
        """Check rank of a player

        :param uuid: The uuid of the player
        """
        uuid = UUID(uuid).no_dashes
        m = [x for x in self.members if x.uuid == uuid]
        if len(m) != 0:
            mem = m[0]
            return [r for r in self.ranks if r.name == mem.rank][0]
        raise NotInGuildException(uuid)

    @property
    def ranks(self) -> List[GuildRank]:
        """The ranks of the guild"""
        tr = []
        i = 0
        for v in self._raw["ranks"]:
            tr.append(v)
            i += 1
        tr.sort(key=lambda x: x["priority"])
        rank_names = [x["name"] for x in tr]
        gm = [x["rank"] for x in self.members if x["rank"] not in rank_names][0]
        tr.append(
            {
                "name": gm,
                "default": False,
                "tag": "GM",
                "created": self._raw["created"],
                "priority": tr[-1]["priority"] + 1,
            }
        )
        return [GuildRank(x, idx) for idx, x in enumerate(tr)]
