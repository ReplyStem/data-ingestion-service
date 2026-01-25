"""
Ingested Message Model.

SQLAlchemy model for the ingested_messages table in ingestion schema.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


def generate_id() -> str:
    """Generate unique message ID."""
    return f"msg_{uuid4().hex[:12]}"


class IngestedMessage(Base):
    """Ingested messages table in ingestion schema."""

    __tablename__ = "ingested_messages"
    __table_args__ = (
        Index("idx_messages_tenant", "tenant_id"),
        Index("idx_messages_platform", "platform"),
        Index("idx_messages_created", "created_at"),
        {"schema": "ingestion"},
    )

    id: Mapped[str] = mapped_column(String(50), primary_key=True, default=generate_id)
    tenant_id: Mapped[str] = mapped_column(String(50), nullable=False)
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    source_id: Mapped[str] = mapped_column(String(255), nullable=False)
    sender_id: Mapped[str] = mapped_column(String(255), nullable=False)
    sender_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), default="text")
    normalized_payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<IngestedMessage(id={self.id}, platform={self.platform})>"
