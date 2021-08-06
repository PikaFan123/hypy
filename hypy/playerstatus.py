from typing import Optional
from .hypyobject import HypyObject


class PlayerStatus(HypyObject):
    """Status of a player"""

    online: bool
    """Whether the player is currently online"""
    game: Optional[str]
    """The game the player is currently playing"""
    mode: Optional[str]
    """The mode of the game the player is currently playing"""
    map: Optional[str]
    """The map the player is currently playing on"""

    def __init__(self, data) -> None:
        self._raw = data["session"]
        self.online = self._raw["online"]
        self.game = self._raw["gameType"] if self.online else None
        self.mode = self._raw["mode"] if self.online else None
        self.map = self._raw["map"] if ("map" in self._raw) else None
