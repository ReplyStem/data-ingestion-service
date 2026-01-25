"""
Platform Types.

Enum for supported platform types matching tenant_service.
"""

from enum import Enum


class PlatformType(str, Enum):
    """Supported platform types."""

    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    WHATSAPP = "whatsapp"
    GOOGLE_PLAY = "google_play"
    APPLE_STORE = "apple_store"
    EMAIL = "email"
    WEB_CHAT = "web_chat"

    @classmethod
    def webhook_platforms(cls) -> list["PlatformType"]:
        """Platforms that use webhooks."""
        return [cls.INSTAGRAM, cls.FACEBOOK, cls.TWITTER, cls.WHATSAPP]

    @classmethod
    def polling_platforms(cls) -> list["PlatformType"]:
        """Platforms that require polling."""
        return [cls.GOOGLE_PLAY, cls.APPLE_STORE]
