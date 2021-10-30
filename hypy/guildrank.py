from datetime import datetime
from .hypyobject import HypyObject


class GuildRank(HypyObject):
    """A Hypixel guild rank"""

    name: str
    """The name of the rank"""
    default: bool
    """Whether the rank is the default rank for the guild"""
    tag: str
    """The tag of the rank"""
    priority: int
    """The priority of the rank"""
    index: int
    """The position of the rank"""

    def __init__(self, raw, idx) -> None:
        self._raw = raw
        self._raw["inGuild"] = True  # backwards compat
        self._raw["rank"] = idx  # backwards compat
        self.name = self._raw["name"]
        self.default = bool(self._raw.get("default", False))
        self.tag = self._raw.get("tag", "")
        self.priority = self._raw.get("priority", 0)
        self.index = idx

    def __getitem__(self, key):
        return self._raw[key]

    def __repr__(self) -> str:
        return f'<hypy.GuildRank name="{self.name}" priority={self.priority} default={self.default} index={self.index}>'

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def created(self) -> datetime:
        """When the rank was created"""
        return datetime.utcfromtimestamp(self._raw["created"] / 1000)
