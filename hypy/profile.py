from typing import Dict
from collections import defaultdict
from orjson import orjson
import aiofiles
from .vars import scs
from .ext.senither.senither import SenitherWeight
from .hypyobject import HypyObject
from .skyblockskills import (
    SkyblockSkills,
    SkyblockSlayers,
    SkyblockBank,
    REGULAR_SKILLS,
    REGULAR_SKILL_FILTER,
)
from .skyblockinventories import SkyblockInventory, SkyblockBackpacks
from .exceptions import MaroNoSuccess


class SkyblockProfile(HypyObject):
    """A Hypixel SkyBlock Profile"""

    __slots__ = (
        "_raw",
        "_raw_member_info",
        "_hypy",
        "_uuid",
    )

    deleted: bool
    """Whether the profile has been deleted"""
    profile_id: str
    """The profile id of the profile"""

    def __init__(self, data, uuid, hypy) -> None:
        self._hypy = hypy
        self._raw = data["profile"]
        self.profile_id = self._raw["profile_id"]
        self._uuid = uuid
        self._raw_member_info = self._raw["members"][uuid]
        self.deleted = False
        if "last_save" not in self._raw_member_info:
            self._deleted = True
            return
        self.last_save = self._raw_member_info["last_save"]
        self.skills_api_on = any(
            [
                (REGULAR_SKILL_FILTER.format(x) in self._raw_member_info)
                for x in REGULAR_SKILLS
            ]
        )
        self.cute_name = None

    def add_cute_name(self, cute_name):
        """add a cute name to this profile"""
        self.cute_name = cute_name

    async def refetch(self) -> None:
        """Refresh the profile"""
        self._raw = (await self._hypy.get_profile_data(self.profile_id))["profile"]
        self._raw_member_info = self._raw["members"][self._uuid]

    async def save_json(self, filename) -> None:
        """Save raw member info to the disk

        :param filename: The name of the file to save to
        """
        async with aiofiles.open(filename, mode="w+") as f:
            await f.write(orjson.dumps(self._raw_member_info, indent=4))

    async def networth(
        self
    ) -> Dict:
        """Gets the networth of a profile from the Hypixel classes SkyHelper API instance, if one exists."""
        return await self._hypy.skyhelper.get_networth(self._uuid, self.profile_id)

    @property
    def senither_weight(self) -> dict:
        """Returns weight in the Senither weight system"""
        senither = SenitherWeight(self)
        return senither.calc_weight()

    @property
    def skills(self) -> SkyblockSkills:
        """Skill levels"""
        return SkyblockSkills(self._raw_member_info, self._hypy, xp=False)

    @property
    def xp(self) -> SkyblockSkills:
        """Skill xp"""
        return SkyblockSkills(self._raw_member_info, self._hypy, xp=True)

    @property
    def sea_creature_kills(self) -> int:
        """Sea creature kills of profile"""
        kills = self.kills
        sc_kills = 0
        for sc in scs:
            sc_kills += kills[sc]
        return int(sc_kills)

    @property
    def slayer(self) -> SkyblockSlayers:
        """Slayers"""
        return SkyblockSlayers(self._raw_member_info)

    @property
    def inventory(self) -> SkyblockInventory:
        """Inventory data"""
        return SkyblockInventory(self._raw_member_info["inv_contents"], "INVENTORY")

    @property
    def backpacks(self) -> SkyblockBackpacks:
        """Skyblock Backpacks"""
        return SkyblockBackpacks(self._raw_member_info["backpack_contents"])

    @property
    def quiver(self) -> SkyblockInventory:
        """Skyblock Quiver"""
        return SkyblockInventory(self._raw_member_info["quiver"], "QUIVER")

    @property
    def ender_chest(self) -> SkyblockInventory:
        """Skyblock Enderchest"""
        return SkyblockInventory(
            self._raw_member_info["ender_chest_contents"], "ENDERCHEST"
        )

    @property
    def personal_vault(self) -> SkyblockInventory:
        """Skyblock Personal Vault"""
        return SkyblockInventory(
            self._raw_member_info["personal_vault_contents"], "PERSONAL_VAULT"
        )

    @property
    def candy_bag(self) -> SkyblockInventory:
        """Skyblock Candy Bag"""
        return SkyblockInventory(
            self._raw_member_info["candy_inventory_contents"], "CANDY_BAG"
        )

    @property
    def talisman_bag(self) -> SkyblockInventory:
        """Skyblock Talisman Bag"""
        return SkyblockInventory(self._raw_member_info["talisman_bag"], "TALISMAN_BAG")

    @property
    def fishing_bag(self) -> SkyblockInventory:
        """Skyblock Fishing Bag"""
        return SkyblockInventory(self._raw_member_info["fishing_bag"], "FISHING_BAG")

    @property
    def potion_bag(self) -> SkyblockInventory:
        """Skyblock Potion Bag"""
        return SkyblockInventory(self._raw_member_info["potion_bag"], "POTION_BAG")

    @property
    def armor(self) -> SkyblockInventory:
        """Armor data"""
        return SkyblockInventory(self._raw_member_info["inv_armor"], "ARMOR")

    @property
    def kills(self) -> defaultdict:
        """Dictionary of mob kills"""
        tr = defaultdict(lambda: 0)
        tr["total"] = self._raw_member_info["stats"]["kills"]
        for key in self._raw_member_info["stats"]:
            keystr = str(key)
            if keystr.startswith("kills_"):
                tr[keystr.replace("kills_", "")] = self._raw_member_info["stats"][
                    keystr
                ]
        return tr

    @property
    def deaths(self) -> defaultdict:
        """Dictionary of deaths"""
        tr = defaultdict(lambda: 0)
        tr["total"] = self._raw_member_info["stats"]["deaths"]
        for key in self._raw_member_info["stats"]:
            keystr = str(key)
            if keystr.startswith("deaths_"):
                tr[keystr.replace("deaths_", "")] = self._raw_member_info["stats"][
                    keystr
                ]
        return tr

    @property
    def purse(self) -> int:
        """Amount of coins in purse"""
        return self._raw_member_info["coin_purse"]

    @property
    def bank(self) -> SkyblockBank:
        """Coins in bank"""
        return SkyblockBank(self._raw)
