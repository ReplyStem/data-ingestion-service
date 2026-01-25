"""
Normalized Message Schema.

Standardized payload that all platforms normalize to.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.platform import PlatformType


class NormalizedMessage(BaseModel):
    """Standardized message format from any platform."""

    id: str = Field(..., description="Unique message ID")
    tenant_id: str = Field(..., description="Tenant ID")
    platform: PlatformType = Field(..., description="Source platform")
    source_id: str = Field(..., description="Original platform message ID")
    sender_id: str = Field(..., description="Sender identifier on platform")
    sender_name: str | None = Field(None, description="Sender display name")
    content: str = Field(..., description="Message content or review text")
    content_type: str = Field(default="text", description="text, image, rating, etc.")
    rating: int | None = Field(None, ge=1, le=5, description="Rating 1-5 for reviews")
    metadata: dict = Field(default_factory=dict, description="Platform-specific data")
    received_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "msg_abc123",
                "tenant_id": "tenant_xyz",
                "platform": "instagram",
                "source_id": "ig_12345",
                "sender_id": "user_456",
                "sender_name": "John Doe",
                "content": "Great product!",
                "content_type": "text",
                "metadata": {"post_id": "post_789"},
                "received_at": "2024-01-05T10:00:00Z",
            }
        }
    )
