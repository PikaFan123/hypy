from dataclasses import dataclass


@dataclass
class KeyStats:
    """API Key Statistics"""

    owner: str
    """The owner of the api key"""
    owner_name: str
    """The name of the owner of the api key"""
    total_uses: int
    """The total uses of the api key"""
    queries_in_past_minute: int
    """The amount of queries of the api key in the past minute"""
    timestamp: int
    """The timestamp of this information"""


@dataclass
class WatchdogStats:
    """Punishment statistics"""

    watchdog_last_minute: int
    """The amount of bans made by watchdog in the last minute"""
    staff_rolling_daily: int
    """The amount of bans made by staff in the past day"""
    watchdog_total: int
    """The total amount of bans made by watchdog"""
    watchdog_rolling_daily: int
    """The amount of bans made by watchdog in the past day"""
    staff_total: int
    """The total amount of bans made by watchdog"""
