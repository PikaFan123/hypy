from typing import Union, List
from enum import Enum, auto
from .auction import Auction
from .uuid import UUID
from .hypyobject import HypyObject


class FilterType(Enum):
    """Types to filter Auctions by"""

    NAME = auto()
    AUCTIONEER = auto()
    LORE = auto()


class SkyblockAuctions(HypyObject):
    """SkyBlock Auction data"""

    __slots__ = ("_raw", "_auctions", "_hypy", "_num")

    def __init__(self, data, auc, hypy) -> None:
        self._raw = data
        self._auctions = auc
        self._num = len(data)
        self._hypy = hypy

    def __len__(self) -> int:
        return self._num

    def __getitem__(self, key) -> Auction:
        return self._auctions[key]

    async def find_auctions(
        self,
        by: Union[str, FilterType] = "name",
        query: str = "",
        case_sensitive: bool = True,
    ) -> List[Auction]:
        """Find Auctions

        :param by: What to filter by
        :param query: The query
        :param case_sensitive: Whether searching should be case sensitive
        """
        if not case_sensitive:
            query = query.lower()
        if isinstance(by, str):
            by = FilterType[str(by).upper()]
        if by == FilterType.NAME:
            return [
                auction
                for auction in self._auctions
                if query
                in (auction.item_name if case_sensitive else auction.item_name.lower())
            ]
        if by == FilterType.AUCTIONEER:
            auc_uuid = UUID(await self._hypy.mojang.name_to_uuid(query)).no_dashes
            return [
                auction
                for auction in self._auctions
                if auc_uuid == auction.auctioneer_uuid.no_dashes
            ]
        if by == FilterType.LORE:
            return [
                auction
                for auction in self._auctions
                if query
                in (
                    auction.safe_item_lore
                    if case_sensitive
                    else auction.safe_item_lore.lower()
                )
            ]
        else:
            return []
