from abc import ABC
from typing import Iterator
from .uuid import UUID


class HypyIterable(ABC):
    """A hypy Iterable"""

    def iter_uuids(self) -> Iterator[UUID]:
        """Iterate over uuids of Iterable"""


class MinecraftPlayer(ABC):
    """A minecraft player"""

    uuid: UUID
