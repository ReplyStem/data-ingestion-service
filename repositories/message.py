"""
Message Repository.

Async data access layer for ingested messages.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.ingested_message import IngestedMessage
from schemas.normalized import NormalizedMessage


class MessageRepository:
    """Repository for message CRUD operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, message: NormalizedMessage) -> IngestedMessage:
        """Create a new ingested message."""
        db_message = IngestedMessage(
            id=message.id,
            tenant_id=message.tenant_id,
            platform=message.platform.value,
            source_id=message.source_id,
            sender_id=message.sender_id,
            sender_name=message.sender_name,
            content=message.content,
            content_type=message.content_type,
            normalized_payload=message.model_dump(mode="json"),
        )
        self.db.add(db_message)
        await self.db.flush()
        await self.db.refresh(db_message)
        return db_message

    async def get_by_id(self, message_id: str) -> IngestedMessage | None:
        """Get message by ID."""
        result = await self.db.execute(
            select(IngestedMessage).where(IngestedMessage.id == message_id)
        )
        return result.scalar_one_or_none()

    async def get_by_source_id(
        self, tenant_id: str, source_id: str
    ) -> IngestedMessage | None:
        """Get message by source platform ID (for deduplication)."""
        result = await self.db.execute(
            select(IngestedMessage).where(
                IngestedMessage.tenant_id == tenant_id,
                IngestedMessage.source_id == source_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_tenant(
        self, tenant_id: str, limit: int = 100
    ) -> list[IngestedMessage]:
        """List messages for a tenant."""
        result = await self.db.execute(
            select(IngestedMessage)
            .where(IngestedMessage.tenant_id == tenant_id)
            .order_by(IngestedMessage.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
