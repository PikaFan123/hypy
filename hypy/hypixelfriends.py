import asyncio
from typing import Iterator, List
from .hypyobject import HypyObject
from .abc import HypyIterable
from .hypixelfriend import HypixelFriend
from .uuid import UUID


class HypixelFriends(HypyObject, HypyIterable):
    """Hypixel Friends of a Player"""

    __slots__ = ("_raw", "_hypy")

    friends: List[HypixelFriend]
    """A list of HypixelFriends"""

    def __init__(self, raw, hypy) -> None:
        self._raw = raw
        self._hypy = hypy
        self.of = UUID(self._raw["uuid"])
        self.friends = [
            HypixelFriend(friend, self.of, hypy) for friend in self._raw["records"]
        ]

    def iter_uuids(self) -> Iterator[UUID]:
        for i in self:
            yield i.uuid

    def __iter__(self) -> Iterator[HypixelFriend]:
        for i in self.friends:
            yield i

    async def names(self) -> List[str]:
        """Return names of all of the friends"""
        return await asyncio.gather(
            *[friend.name() for friend in sorted(self.friends, key=lambda f: f.since)]
        )
