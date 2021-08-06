from typing import Iterator
from datetime import datetime
from .hypyobject import HypyObject
from .bazaaritem import BazaarItem


class Bazaar(HypyObject):
    """A class containing information about the Hypixel Skyblock bazaar

    Items can be accessed with Bazaar['ITEM_NAME']
    """

    def __init__(self, raw) -> None:
        self._raw = raw
        self._timestamp = self._raw["lastUpdated"]
        self._items = [
            BazaarItem(item_data) for item_data in self._raw["products"].values()
        ]

    def __getitem__(self, key) -> BazaarItem:
        return self._items[key]

    def __iter__(self) -> Iterator[BazaarItem]:
        for i in self._items:
            yield i

    @property
    def timestamp(self) -> datetime:
        """The time when Bazaar information was fetched"""
        return datetime.utcfromtimestamp(self._timestamp / 1000)
