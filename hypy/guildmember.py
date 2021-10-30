from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from .hypyobject import HypyObject
from .hypixelplayer import HypixelPlayer

if TYPE_CHECKING:
    from .guild import Guild
    from .guildrank import GuildRank

class GuildMember(HypixelPlayer, HypyObject):
    """A Hypixel Guild Member"""

    rank: GuildRank
    """The GuildRank of this GuildMember"""

    def __init__(self, raw, guild: Guild, hypy) -> None:
        self._raw = raw
        self._hypy = hypy
        self.uuid = self._raw["uuid"]
        self.rank = guild.rank_of(self)
        self.quest_participation = int(self._raw.get("questParticipation") or 0)
        self.exp_history = self._raw["expHistory"]

    def __getitem__(self, key):
        return self._raw[key]

    @property
    def joined(self) -> datetime:
        """The datetime when the player joined the guild"""
        return datetime.utcfromtimestamp(self._raw["joined"] / 1000)
