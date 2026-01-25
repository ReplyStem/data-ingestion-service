"""
Google Play Worker.

Polls Google Play Store for app reviews.
"""

import logging

from workers.base import BasePollingWorker
from normalizers import normalize_app_review
from schemas.normalized import NormalizedMessage
from schemas.platform import PlatformType

logger = logging.getLogger(__name__)


class GooglePlayWorker(BasePollingWorker):
    """Worker for polling Google Play reviews."""

    platform = PlatformType.GOOGLE_PLAY

    async def fetch_reviews(
        self, tenant_id: str, credentials: dict
    ) -> list[NormalizedMessage]:
        """Fetch reviews from Google Play."""
        messages = []

        # TODO: Implement actual Google Play API integration
        # Requires: package_name, service_account_json from credentials
        package_name = credentials.get("package_name", "")
        logger.info(f"Polling Google Play reviews for {package_name}")

        # Mock response for development
        mock_reviews = [
            {
                "id": "gp_review_001",
                "author_id": "user123",
                "author_name": "John D.",
                "body": "Great app, very useful!",
                "rating": 5,
                "app_version": "1.2.3",
            }
        ]

        for review in mock_reviews:
            normalized = normalize_app_review(tenant_id, self.platform, review)
            messages.append(normalized)

        logger.info(f"Fetched {len(messages)} Google Play reviews")
        return messages

    async def get_last_sync_time(self, tenant_id: str) -> str | None:
        """Get last sync timestamp."""
        # TODO: Implement persistence for sync state
        return None
