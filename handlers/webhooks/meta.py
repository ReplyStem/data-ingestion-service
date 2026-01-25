"""
Meta Webhook Handler.

Handles Facebook and Instagram webhook events.
"""

import hashlib
import hmac
import logging

from handlers.base import BaseWebhookHandler
from normalizers import normalize_meta_message
from schemas.normalized import NormalizedMessage
from schemas.platform import PlatformType

logger = logging.getLogger(__name__)


class MetaWebhookHandler(BaseWebhookHandler):
    """Handler for Meta (Facebook/Instagram) webhooks."""

    def __init__(self, app_secret: str = ""):
        self.app_secret = app_secret

    async def validate_signature(self, payload: bytes, signature: str) -> bool:
        """Validate X-Hub-Signature-256 header."""
        if not self.app_secret:
            logger.warning("No app secret configured, skipping validation")
            return True

        expected = "sha256=" + hmac.new(
            self.app_secret.encode(), payload, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    async def process(
        self, tenant_id: str, payload: dict
    ) -> list[NormalizedMessage]:
        """Process Meta webhook payload."""
        messages = []
        obj_type = payload.get("object", "")

        platform = (
            PlatformType.INSTAGRAM if obj_type == "instagram" else PlatformType.FACEBOOK
        )

        for entry in payload.get("entry", []):
            for msg in entry.get("messaging", []):
                if "message" in msg:
                    normalized = normalize_meta_message(tenant_id, platform, entry, msg)
                    messages.append(normalized)
                    logger.info(f"Normalized Meta message: {normalized.id}")

        return messages
