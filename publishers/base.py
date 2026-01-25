"""
Base Publisher.

Abstract interface for message publishing (SQS, Kafka, etc.).
"""

from abc import ABC, abstractmethod

from schemas.normalized import NormalizedMessage


class BasePublisher(ABC):
    """Abstract base class for message publishers."""

    @abstractmethod
    async def publish(self, message: NormalizedMessage) -> bool:
        """Publish a normalized message. Returns True on success."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if publisher is healthy."""
        pass
