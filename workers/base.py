"""
Base Polling Worker.

Abstract interface for platform polling workers.
"""

from abc import ABC, abstractmethod

from schemas.normalized import NormalizedMessage
from schemas.platform import PlatformType


class BasePollingWorker(ABC):
    """Abstract base class for polling workers."""

    platform: PlatformType

    @abstractmethod
    async def fetch_reviews(
        self, tenant_id: str, credentials: dict
    ) -> list[NormalizedMessage]:
        """Fetch and normalize reviews from platform."""
        pass

    @abstractmethod
    async def get_last_sync_time(self, tenant_id: str) -> str | None:
        """Get last sync timestamp for incremental polling."""
        pass
