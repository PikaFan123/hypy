from .vars import cata_xp_cumulative
from .hypyobject import HypyObject


class SkyBlockResources(HypyObject):
    """Hypixel SkyBlock resources"""

    __slots__ = ("_raw", "cumulative_xp")

    def __init__(self, data) -> None:
        self._raw = data["skills"]
        self.update_cumulative_xp()

    def update_cumulative_xp(self) -> None:
        """Update Internal cumulative XP Tables"""
        cumu_xp: dict = {}
        for skill, values in self._raw.items():
            i_skill = str.lower(skill)
            cumu_xp[i_skill] = {}
            cumu_xp[i_skill]["details"] = {}
            cumu_xp[i_skill]["levels"] = {0: 0}
            cumu_xp[i_skill]["details"]["max_level"] = values["maxLevel"]
            for level in values["levels"]:
                cumu_xp[i_skill]["levels"][level["level"]] = int(
                    level["totalExpRequired"]
                )
        cumu_xp["catacombs"] = {}
        cumu_xp["catacombs"]["levels"] = cata_xp_cumulative
        cumu_xp["catacombs"]["details"] = {"max_level": 50}
        self.cumulative_xp = cumu_xp
