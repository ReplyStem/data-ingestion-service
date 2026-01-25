"""
Twitter Webhook Handler.

Handles X/Twitter webhook events with CRC validation.
"""

import base64
import hashlib
import hmac
import logging

from handlers.base import BaseWebhookHandler
from normalizers import normalize_twitter_dm
from schemas.normalized import NormalizedMessage

logger = logging.getLogger(__name__)


class TwitterWebhookHandler(BaseWebhookHandler):
    """Handler for Twitter/X webhooks."""

    def __init__(self, consumer_secret: str = ""):
        self.consumer_secret = consumer_secret

    def create_crc_response(self, crc_token: str) -> str:
        """Create CRC response token for Twitter webhook verification."""
        if not self.consumer_secret:
            return ""

        sha256_hash = hmac.new(
            self.consumer_secret.encode(),
            crc_token.encode(),
            hashlib.sha256,
        ).digest()
        return "sha256=" + base64.b64encode(sha256_hash).decode()

    async def validate_signature(self, payload: bytes, signature: str) -> bool:
        """Validate X-Twitter-Webhooks-Signature header."""
        if not self.consumer_secret:
            logger.warning("No consumer secret configured, skipping validation")
            return True

        expected = "sha256=" + base64.b64encode(
            hmac.new(
                self.consumer_secret.encode(), payload, hashlib.sha256
            ).digest()
        ).decode()
        return hmac.compare_digest(expected, signature)

    async def process(
        self, tenant_id: str, payload: dict
    ) -> list[NormalizedMessage]:
        """Process Twitter webhook payload."""
        messages = []

        for event in payload.get("direct_message_events", []):
            if event.get("type") == "message_create":
                normalized = normalize_twitter_dm(tenant_id, event)
                messages.append(normalized)
                logger.info(f"Normalized Twitter DM: {normalized.id}")

        return messages
