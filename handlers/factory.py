"""
Handler Factory.

Factory manager for creating platform-specific handlers.
"""

from handlers.base import BaseWebhookHandler
from handlers.webhooks.meta import MetaWebhookHandler
from handlers.webhooks.twitter import TwitterWebhookHandler
from schemas.platform import PlatformType


class HandlerFactory:
    """Factory for creating platform handlers."""

    _webhook_handlers: dict[PlatformType, type[BaseWebhookHandler]] = {
        PlatformType.INSTAGRAM: MetaWebhookHandler,
        PlatformType.FACEBOOK: MetaWebhookHandler,
        PlatformType.TWITTER: TwitterWebhookHandler,
    }

    @classmethod
    def get_webhook_handler(
        cls, platform: PlatformType, credentials: dict | None = None
    ) -> BaseWebhookHandler:
        """Get webhook handler for platform."""
        handler_class = cls._webhook_handlers.get(platform)
        if not handler_class:
            raise ValueError(f"No webhook handler for platform: {platform}")

        credentials = credentials or {}

        if platform in (PlatformType.INSTAGRAM, PlatformType.FACEBOOK):
            return handler_class(app_secret=credentials.get("app_secret", ""))
        elif platform == PlatformType.TWITTER:
            return handler_class(consumer_secret=credentials.get("consumer_secret", ""))

        return handler_class()

    @classmethod
    def supports_webhook(cls, platform: PlatformType) -> bool:
        """Check if platform supports webhooks."""
        return platform in cls._webhook_handlers
