from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from .abc import MinecraftPlayer

if TYPE_CHECKING:
    from .hypixel import Hypixel
    from .hypixelfriends import HypixelFriends
    from .guild import Guild
    from .playerstatus import PlayerStatus
    from .player import Player


class HypixelPlayer(MinecraftPlayer):
    """Class for HypixelPlayer-likes to inherit from"""

    _hypy: Hypixel

    async def friends(self) -> HypixelFriends:
        """Gets HypixelFriends of the HypixelPlayer"""
        return await self._hypy.get_friends(str(self.uuid))

    async def status(self) -> PlayerStatus:
        """Gets PlayerStatus of the HypixelPlayer"""
        return await self._hypy.get_player_status(str(self.uuid))

    async def guild(self) -> Optional[Guild]:
        """Gets the Guild of the HypixelPlayer"""
        return await self._hypy.get_guild(playerNameOrUuid=str(self.uuid))

    async def player(self) -> Player:
        """Gets the Player of the HypixelPlayer"""
        return await self._hypy.get_player(nameOrUuid=str(self.uuid))

    async def name(self) -> str:
        """Gets the Name of the HypixelPlayer from the Mojang API"""
        return await self._hypy.mojang.uuid_to_name(str(self.uuid))
