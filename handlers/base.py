"""
Base Webhook Handler.

Abstract interface for platform-specific webhook handlers.
"""

from abc import ABC, abstractmethod

from schemas.normalized import NormalizedMessage


class BaseWebhookHandler(ABC):
    """Abstract base class for webhook handlers."""

    @abstractmethod
    async def validate_signature(self, payload: bytes, signature: str) -> bool:
        """Validate webhook signature."""
        pass

    @abstractmethod
    async def process(
        self, tenant_id: str, payload: dict
    ) -> list[NormalizedMessage]:
        """Process webhook payload and return normalized messages."""
        pass
