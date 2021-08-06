from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple
from datetime import datetime
from itertools import chain
from .uuid import UUID
from .hypyobject import HypyObject
from .utils import unpack_nbt, decode_nbt, get_auction_lores
from .skyblockinventories import SkyblockItemSlot

if TYPE_CHECKING:
    from .hypixel import Hypixel

USE_NBT = False


def multi_init(pages: List[dict], hypy: Hypixel) -> Tuple[List[dict], List[Auction]]:
    """initialize multiple auctions at once"""
    auctions = list(
        chain.from_iterable([x["auctions"] for x in pages])
    )  # join all auctions from all pages into one list
    lores = get_auction_lores(auctions)
    return (
        auctions,
        [Auction.init(info[0], info[1], hypy) for info in zip(auctions, lores)],
    )


class Auction(HypyObject):
    """A Hypixel SkyBlock Auction"""

    _uuid: str
    _raw: dict
    _hypy: Hypixel
    auctioneer_uuid: UUID
    """The UUID of the auctioneer"""
    profile_id: str
    """The profile id of the auctioneer"""
    _start: int
    _end: int
    item_name: str
    """The name of the item"""
    item_lore: str
    """The lore of the item
    If you want cleaned lore (without colorcodes) use `safe_item_lore` instead
    """
    safe_item_lore: str
    """The lore without any formatting"""
    item_category: str
    """The auction house category of the item"""
    tier: str
    """The rarity of the item"""
    starting_bid: str
    """The starting bid of the item"""
    _bytes: str
    bin: bool
    """Whether the auction is BIN (Buy it now) or not"""
    highest_bid: int
    """The highest bid of the auction"""

    def __init__(self, data, hypy) -> None:
        self._hypy = hypy
        self._raw = data
        self._uuid = data["uuid"]
        self.auctioneer_uuid = UUID(data["auctioneer"])
        self._start = data["start"]
        self._end = data["end"]
        self._bytes = data["item_bytes"]

    @staticmethod
    def init(data, lore, hypy) -> Auction:
        """Initialize an Auction object"""
        auc = Auction(data, hypy)
        auc.profile_id = data["profile_id"]
        auc.item_name = data["item_name"]
        auc.item_lore = data["item_lore"]
        auc.safe_item_lore = lore
        auc.item_category = data["category"]
        auc.tier = data["tier"]
        auc.starting_bid = data["starting_bid"]
        auc.bin = data["bin"] if ("bin" in data) else False
        auc.highest_bid = data["highest_bid_amount"]
        return auc

    def __str__(self) -> str:
        return f"<hypy.Auction item_name={self.item_name}>"

    @property
    def nbt_item(self) -> SkyblockItemSlot:
        """A SkyblockItemSlot for this auction"""
        return SkyblockItemSlot(unpack_nbt(decode_nbt(self._raw["item_bytes"]))["i"][0])

    @property
    def start(self) -> datetime:
        """The start of the auction"""
        return datetime.utcfromtimestamp(self._start / 1000)

    @property
    def end(self) -> datetime:
        """The end of the auction"""
        return datetime.utcfromtimestamp(self._end / 1000)

    async def get_auctioneer_name(self) -> str:
        """Get name of Auctioneer

        Returns:
            The name of the auctioneer

        Raises:
            UUIDNotFound: The uuid to find the name was invalid
        """
        return await self._hypy.mojang.uuid_to_name(self.auctioneer_uuid.no_dashes)
