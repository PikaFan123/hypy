from typing import List
from .hypyobject import HypyObject


class BazaarOrder(HypyObject):
    """An order on the SkyBlock Bazaar"""

    type: str
    """Whether the order is a BUY or SELL order"""
    price_per_unit: int
    """The price per item"""
    amount: int
    """The amount of items ordered"""

    def __init__(self, raw: dict, order_type: str, item: str) -> None:
        self._raw = raw
        self.type = order_type
        self.item = item
        self.price_per_unit = self._raw["pricePerUnit"]
        self.orders = self._raw["orders"]
        self.amount = self._raw["amount"]

    def __repr__(self) -> str:
        return f"<hypy.BazaarOrder item={self.item} type={self.type} price_per_unit={self.price_per_unit} amount={self.amount}>"


class BazaarItem(HypyObject):
    """An item on the SkyBlock Bazaar"""

    product_id: str
    """The items id"""
    buy_orders: List[BazaarOrder]
    """A list of buy orders for the item"""
    sell_orders: List[BazaarOrder]
    """A list of sell orders for the item"""

    def __init__(self, raw: dict) -> None:
        self._raw = raw
        self.product_id = self._raw["product_id"]
        self.buy_orders = [
            BazaarOrder(data, "BUY", self.product_id)
            for data in self._raw["buy_summary"]
        ]
        self.buy_orders = [
            BazaarOrder(data, "SELL", self.product_id)
            for data in self._raw["sell_summary"]
        ]

    def __repr__(self) -> str:
        return f"<hypy.BazaarItem item={self.product_id}>"
