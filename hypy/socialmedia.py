from typing import Optional


class SocialMedia:
    """Hypixel Social Media response wrapper"""

    def __init__(self, raw):
        self._raw = raw

    def _get_social(self, social) -> Optional[str]:
        if "socialMedia" not in self._raw:
            return None
        if "links" not in self._raw["socialMedia"]:
            return None
        if social not in self._raw["socialMedia"]["links"]:
            return None
        return str(self._raw["socialMedia"]["links"][social]).strip()

    @property
    def youtube(self) -> Optional[str]:
        """The linked youtube channel"""
        return self._get_social("YOUTUBE")

    @property
    def discord(self) -> Optional[str]:
        """The linked discord tag"""
        return self._get_social("DISCORD")

    @property
    def hypixel(self) -> Optional[str]:
        """The linked hypixel forums account"""
        return self._get_social("HYPIXEL")

    @property
    def mixer(self) -> Optional[str]:
        """The linked mixer account"""
        # did you know you could link mixer? cause i sure didnt.
        return self._get_social("MIXER")

    @property
    def twitch(self) -> Optional[str]:
        """The linked twitch account"""
        return self._get_social("TWITCH")

    @property
    def twitter(self) -> Optional[str]:
        """The linked twitter account"""
        return self._get_social("TWITTER")

    @property
    def instagram(self) -> Optional[str]:
        """The linked instagram account"""
        return self._get_social("INSTAGRAM")
