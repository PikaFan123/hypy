from typing import Any, Optional
from .hypyobject import HypyObject

REGULAR_SKILLS = [
    "fishing",
    "alchemy",
    "taming",
    "enchanting",
    "combat",
    "mining",
    "farming",
    "foraging",
]

COSMETIC_SKILLS = [
    "carpentry",
    "runecrafting",
    "social"
]

REGULAR_SKILL_FILTER = "experience_skill_{}"

DUNGEON_SKILLS = ["catacombs"]

CLASS_SKILLS = ["healer", "berserk", "archer", "mage", "tank"]

SLAYER_TYPES = ["zombie", "spider", "wolf", "enderman"]


class SkyblockSkills(HypyObject):
    """A class representing skyblock skills

    The level of a skill can be retrieved like this: skyblockskills.fishing
    """

    __slots__ = REGULAR_SKILLS + DUNGEON_SKILLS + CLASS_SKILLS

    def __init__(self, raw, hypy, xp=False) -> None:
        self._profile_info = raw
        self._hypy = hypy
        self._xp = xp

    @property
    def raw(self) -> dict:
        """Get skills in a dictionary style"""
        return {
            "detail": {
                "fishing": self.fishing,
                "alchemy": self.alchemy,
                "taming": self.taming,
                "enchanting": self.enchanting,
                "combat": self.combat,
                "mining": self.mining,
                "farming": self.farming,
                "foraging": self.foraging,
                "catacombs": self.catacombs,
            },
            "avg": self.avg,
            "classes": {
                "healer": self.healer,
                "berserk": self.berserk,
                "archer": self.archer,
                "mage": self.mage,
                "tank": self.tank,
            },
            "misc": {"carpentry": self.carpentry, "runecrafting": self.runecrafting, "social": self.social},
        }

    @property
    def _raw(self):
        return self.raw

    def __getitem__(self, key) -> Any:
        return self._raw[key]

    def __getattr__(self, name) -> float:
        try:
            return self._get_skill_info(name)
        except KeyError:
            return 0.0

    def _get_skill_info(self, skill) -> float:
        if skill in REGULAR_SKILLS + COSMETIC_SKILLS:
            return float(self._get_regular_skill_info(skill))
        if skill in DUNGEON_SKILLS:
            return float(self._get_dungeon_skill_info(skill))
        if skill in CLASS_SKILLS:
            return float(self._get_class_skill_info(skill))
        if skill == "avg":
            return sum([self.__getattr__(x) for x in REGULAR_SKILLS]) / len(
                REGULAR_SKILLS
            )
        return 0.0

    def _get_regular_skill_info(self, skill) -> float:
        if REGULAR_SKILL_FILTER.format(skill) in self._profile_info:
            if self._xp:
                return self._profile_info[REGULAR_SKILL_FILTER.format(skill)]
            return self._hypy.utils.lvlCalc(
                self._profile_info[REGULAR_SKILL_FILTER.format(skill)], skill
            )
        return 0.0

    def _get_dungeon_skill_info(self, skill) -> float:
        if "dungeons" not in self._profile_info:
            return 0.0
        if skill not in self._profile_info["dungeons"]["dungeon_types"]:
            return 0.0
        if "experience" not in self._profile_info["dungeons"]["dungeon_types"][skill]:
            return 0.0
        if self._xp:
            return self._profile_info["dungeons"]["dungeon_types"][skill]["experience"]
        return self._hypy.utils.lvlCalc(
            self._profile_info["dungeons"]["dungeon_types"][skill]["experience"], skill
        )

    def _get_class_skill_info(self, skill) -> float:
        if "dungeons" not in self._profile_info:
            return 0.0
        if "player_classes" not in self._profile_info["dungeons"]:
            return 0.0
        if skill not in self._profile_info["dungeons"]["player_classes"]:
            return 0.0
        if "experience" not in self._profile_info["dungeons"]["player_classes"][skill]:
            return 0.0
        if self._xp:
            return self._profile_info["dungeons"]["player_classes"][skill]["experience"]
        return self._hypy.utils.lvlCalc(
            self._profile_info["dungeons"]["player_classes"][skill]["experience"],
            "catacombs",
        )


class SkyblockSlayers(HypyObject):
    """A class representing Skyblock Slayers of a profile

    The xp of a slayer can be retrieved like this: skyblockskills.enderman
    """

    def __init__(self, raw):
        self._profile_info = raw
        self._slayer_info = self._profile_info["slayer_bosses"]

    @property
    def raw(self) -> dict:
        """Get slayers in a dictionary style"""
        return {
            "detail": {
                "wolf": self.wolf,
                "enderman": self.enderman,
                "spider": self.spider,
                "zombie": self.zombie,
            },
            "total": self.total,
        }

    @property
    def _raw(self):
        return self.raw

    def __getitem__(self, key) -> int:
        return self._raw[key]

    def __getattr__(self, name) -> int:
        try:
            if name == "total":
                return sum([self.__getattr__(x) for x in SLAYER_TYPES])
            return self._get_slayer_info(name)
        except KeyError:
            return 0

    def _get_slayer_info(self, slayer_type):
        if slayer_type not in self._slayer_info:
            return 0
        if "xp" not in self._slayer_info[slayer_type]:
            return 0
        return self._slayer_info[slayer_type]["xp"]


class SkyblockBank(HypyObject):
    """A class representing the skyblock bank of a profile"""

    def __init__(self, raw) -> None:
        self._raw_data = raw
        self._api_on = "banking" in self._raw_data

    @property
    def _raw(self):
        return self.raw

    @property
    def raw(self) -> dict:
        """A dict style representation of SkyblockBank"""
        return {
            "balance": self.balance or 0,
            "msg": "-" if self._api_on else "API is off",
            "success": self._api_on,
        }

    def __getitem__(self, key):
        return self.raw[key]

    @property
    def balance(self) -> Optional[int]:
        """Balance in bank"""
        if self._api_on:
            return self._raw_data["banking"]["balance"]
        return None
