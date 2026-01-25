"""
Apple App Store Worker.

Polls Apple App Store Connect for app reviews.
"""

import logging

from workers.base import BasePollingWorker
from normalizers import normalize_app_review
from schemas.normalized import NormalizedMessage
from schemas.platform import PlatformType

logger = logging.getLogger(__name__)


class AppleStoreWorker(BasePollingWorker):
    """Worker for polling Apple App Store reviews."""

    platform = PlatformType.APPLE_STORE

    async def fetch_reviews(
        self, tenant_id: str, credentials: dict
    ) -> list[NormalizedMessage]:
        """Fetch reviews from App Store Connect."""
        messages = []

        # TODO: Implement actual App Store Connect API integration
        # Requires: key_id, issuer_id, private_key from credentials
        app_id = credentials.get("app_id", "")
        logger.info(f"Polling App Store reviews for app {app_id}")

        # Mock response for development
        mock_reviews = [
            {
                "id": "as_review_001",
                "reviewerNickname": "AppFan",
                "text": "Love this app!",
                "score": 5,
                "reviewerVersion": "2.0.0",
                "title": "Amazing app",
            }
        ]

        for review in mock_reviews:
            normalized = normalize_app_review(tenant_id, self.platform, review)
            messages.append(normalized)

        logger.info(f"Fetched {len(messages)} App Store reviews")
        return messages

    async def get_last_sync_time(self, tenant_id: str) -> str | None:
        """Get last sync timestamp."""
        # TODO: Implement persistence for sync state
        return None
