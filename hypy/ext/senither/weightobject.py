from dataclasses import dataclass


@dataclass
class WeightObject:
    """A senither weight object"""

    weight = 0.0
    overflow = 0.0

    def __str__(self) -> str:
        return f"<hypy.ext.WeightObject weight={self.weight} overflow={self.overflow}>"
