import uuid as uuidc


class UUID:
    """Helper Class for uuid"""

    def __init__(self, uuid):
        self.uuid = uuidc.UUID(uuid)

    @property
    def dashes(self) -> str:
        """The UUID with dashes"""
        return str(self.uuid)

    @property
    def no_dashes(self) -> str:
        """The UUID without dashes"""
        return str(self.uuid).replace("-", "")

    def __str__(self) -> str:
        return self.no_dashes

    def __eq__(self, other) -> bool:
        return str(self) == str(UUID(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return f"<hypy.UUID uuid={str(self.no_dashes)}>"
