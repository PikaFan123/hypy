from typing import Iterator, List, Dict
from .utils import unpack_nbt, decode_nbt, parse_timestamp


class SkyblockItemSlot:
    """A Skyblock Item Slot"""

    empty: bool = False
    """Whether the slot is empty"""
    enchantments: Dict[str, int] = {}
    """A dictionary of enchantments (name:level)"""
    origin: str = ""
    """How the item was obtained"""
    name: str = ""
    """The name of the item"""
    lore: str = ""
    """The lore of the item"""
    skyblock_item_id: str = ""
    """The skyblock item id of the item"""
    minecraft_item_id: int = 0
    """The minecraft item id of the item"""
    reforge: str = ""
    """The reforge of the item"""
    recombobulated: bool = False
    """Whether the items rarity has been upgraded"""
    count: int = 0
    """How many items there are"""

    def __init__(self, raw) -> None:
        self._raw = raw
        if not bool(self._raw):
            self.empty = True
            return
        self.minecraft_item_id = self._raw["id"]
        self.count = self._raw["Count"]
        self.damage = self._raw["Damage"]
        self.name = self._raw["tag"]["display"]["Name"]
        self.lore = self._raw["tag"]["display"]["Lore"]
        self.skyblock_item_id = self._raw["tag"]["ExtraAttributes"].get("id")
        self.uuid = self._raw["tag"]["ExtraAttributes"].get("uuid")
        self.reforge = self._raw["tag"]["ExtraAttributes"].get("modifier")
        self.recombobulated = bool(
            self._raw["tag"]["ExtraAttributes"].get("rarity_upgrades", False)
        )
        self.enchantments = self._raw["tag"]["ExtraAttributes"].get("enchantments")
        self.origin = self._raw["tag"]["ExtraAttributes"].get("originTag")
        self.timestamp = "timestamp" in self._raw["tag"][
            "ExtraAttributes"
        ] and parse_timestamp(self._raw["tag"]["ExtraAttributes"]["timestamp"])

    def __repr__(self) -> str:
        return f"<hypy.SkyBlockItemSlot empty={self.empty} skyblock_item_id={self.skyblock_item_id}>"

    def __str__(self) -> str:
        return self.__repr__()


class SkyblockInventory:
    """A Skyblock Inventory"""

    type: str
    """The type of the inventory"""
    slots: List[SkyblockItemSlot]
    """The list of items in the inventory"""

    def __init__(self, raw, inventory_type) -> None:
        self._raw = raw
        self.type = inventory_type
        self.nbt_data = unpack_nbt(decode_nbt(self._raw["data"]))["i"]
        self.slots = [SkyblockItemSlot(x) for x in self.nbt_data]

    def __repr__(self) -> str:
        return f"<hypy.SkyblockInventory type={self.type} slot_count={len(self)}>"

    def __len__(self) -> int:
        return len(self.slots)

    def __getitem__(self, key) -> SkyblockItemSlot:
        return self.slots[key]

    def __iter__(self) -> Iterator[SkyblockItemSlot]:
        for i in self.slots:
            yield i


class SkyblockBackpack(SkyblockInventory):
    """A Skyblock Backpack"""

    def __init__(self, raw, inventory_type, backpack_index) -> None:
        super().__init__(raw, "BACKPACK")
        self.backpack_index = backpack_index


class SkyblockBackpacks:
    """A list of SkyBlock backpacks"""

    backpacks: List[SkyblockBackpack]
    """A list of SkyblockBackpacks"""

    def __init__(self, raw) -> None:
        self._raw = raw
        self.backpacks = [
            SkyblockBackpack(v, "BACKPACK", int(k))
            for k, v in sorted(self._raw.items(), key=lambda x: int(x[0]))
        ]

    def __len__(self) -> int:
        return len(self.backpacks)

    def __getitem__(self, key) -> SkyblockBackpack:
        return self.backpacks[key]

    def __iter__(self) -> Iterator[SkyblockBackpack]:
        for i in self.backpacks:
            yield i
