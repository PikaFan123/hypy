from math import floor
from .vars import (
    dungeon_weights,
    slayer_weights,
    skill_weights,
    lvl50,
    lvl60,
    skills,
    slayers,
    lvl50dung,
    classes,
)
from .weightobject import WeightObject


class SenitherWeight:
    """Senither Weight Object"""

    def __init__(self, profile) -> None:
        self._profile = profile

    def _get_skill_weight(self) -> WeightObject:
        """Calculate skill weight"""
        weight_object = WeightObject()
        levels = self._profile.skills["detail"]
        xps = self._profile.xp["detail"]
        for skill in skills:
            skill_weight = skill_weights[skill]
            max_xp = lvl60 if (skill_weight["lvl_cap"] == 60) else lvl50
            xp = xps[skill]
            lvl = levels[skill]
            base = pow(lvl * 10, 0.5 + skill_weight["expo"] + lvl / 100) / 1250
            if xp > max_xp:
                base = round(base)
            if xp <= max_xp:
                weight_object.weight += base
                continue
            weight_object.weight += base
            weight_object.overflow += pow((xp - max_xp) / skill_weight["divr"], 0.968)
        return weight_object

    def _get_slayer_weight(self) -> WeightObject:
        """Calculate slayer weight"""
        weight_object = WeightObject()
        slayer_data = self._profile.slayer["detail"]
        for slayer in slayers:
            divider = slayer_weights[slayer]["divr"]
            mod = slayer_weights[slayer]["mod"]
            omod = mod
            xp = slayer_data[slayer]
            if xp <= 1000000:
                weight_object.weight += 0 if xp == 0 else xp / divider
                continue
            overflow = 0
            base = 1000000 / divider
            remaining = xp - 1000000
            while remaining > 0:
                left = min(remaining, 1000000)
                overflow += pow(left / (divider * (1.5 + mod)), 0.942)
                mod += omod
                remaining -= left
            weight_object.weight += base + overflow
        return weight_object

    def _get_dungeon_weight(self) -> WeightObject:
        """Calculate dungeon weight"""
        weight_object = WeightObject()
        levels = self._profile.skills.raw
        levels["classes"]["catacombs"] = levels["detail"]["catacombs"]
        xps = self._profile.xp.raw
        xps["classes"]["catacombs"] = xps["detail"]["catacombs"]
        for dclass in classes:
            per_mod = dungeon_weights[dclass]
            xp = xps["classes"][dclass]
            lvl = levels["classes"][dclass]
            base = pow(lvl, 4.5) * per_mod
            if xp <= lvl50dung:
                weight_object.weight += base
                continue
            remaining = xp - lvl50dung
            splitter = (4 * lvl50dung) / base
            weight_object.weight += floor(base)
            weight_object.overflow += pow(remaining / splitter, 0.968)
        return weight_object

    def calc_weight(self) -> dict:
        """Calculate Senither weight"""
        skill_weight = self._get_skill_weight()
        slayer_weight = self._get_slayer_weight()
        dungeon_weight = self._get_dungeon_weight()

        total_weight = (
            skill_weight.weight + slayer_weight.weight + dungeon_weight.weight
        )
        total_overflow = (
            skill_weight.overflow + slayer_weight.overflow + dungeon_weight.overflow
        )
        return {
            "total": total_weight + total_overflow,
            "weight": total_weight,
            "overflow": total_overflow,
            "skills": skill_weight.weight,
            "slayers": slayer_weight.weight,
            "dungeons": dungeon_weight.weight,
        }
