from .hypyobject import HypyObject


class PlayerCounts(HypyObject):
    """Hypixel Player counts

    Get the counts of a game with playercounts.GAME_NAME
    """

    def __init__(self, raw) -> None:
        self._raw = raw

    def __int__(self) -> int:
        return self._raw["playerCount"]

    def __getattr__(self, name) -> int:
        return self._raw["games"][name.upper()]["players"]
