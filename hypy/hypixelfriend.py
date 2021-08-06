from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from .hypyobject import HypyObject
from .uuid import UUID
from .hypixelplayer import HypixelPlayer

if TYPE_CHECKING:
    from .player import Player
    from .hypixelfriends import HypixelFriends


class HypixelFriend(HypyObject, HypixelPlayer):
    """A Hypixel Friend"""

    __slots__ = ("_raw", "_hypy", "_id")

    def __init__(self, raw, of, _hypy) -> None:
        self._raw: dict = raw
        self._hypy = _hypy
        self.of = of
        self._id = self._raw["_id"]
        self.uuid = UUID(
            self._raw["uuidReceiver"]
            if of.no_dashes == self._raw["uuidSender"]
            else self._raw["uuidSender"]
        )

    @property
    def since(self) -> datetime:
        """Since when the friendship exists"""
        return datetime.utcfromtimestamp(self._raw["started"] / 1000)
