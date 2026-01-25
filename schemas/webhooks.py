"""
Webhook Request Schemas.

Platform-specific webhook payload schemas.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class MetaWebhookEntry(BaseModel):
    """Single entry in Meta webhook payload."""

    id: str
    time: int
    messaging: list[dict] = Field(default_factory=list)
    changes: list[dict] = Field(default_factory=list)


class MetaWebhookPayload(BaseModel):
    """Meta (Facebook/Instagram) webhook payload."""

    object: str = Field(..., description="instagram or page")
    entry: list[MetaWebhookEntry] = Field(default_factory=list)


class TwitterCRCPayload(BaseModel):
    """Twitter CRC challenge payload."""

    crc_token: str


class TwitterWebhookEvent(BaseModel):
    """Twitter webhook event payload."""

    for_user_id: str = Field(..., description="User ID receiving event")
    direct_message_events: list[dict] = Field(default_factory=list)
    tweet_create_events: list[dict] = Field(default_factory=list)


class WebhookResponse(BaseModel):
    """Standard webhook response."""

    status: str = "ok"
    message_id: str | None = None
    processed_at: datetime = Field(default_factory=datetime.utcnow)
