"""
Data Normalizer.

Transforms platform-specific payloads into standardized format.
"""

from datetime import datetime
from uuid import uuid4

from schemas.normalized import NormalizedMessage
from schemas.platform import PlatformType


def generate_message_id() -> str:
    """Generate unique message ID."""
    return f"msg_{uuid4().hex[:12]}"


def normalize_meta_message(
    tenant_id: str, platform: PlatformType, entry: dict, message: dict
) -> NormalizedMessage:
    """Normalize Meta (Facebook/Instagram) message."""
    sender = message.get("sender", {})
    msg_data = message.get("message", {})

    return NormalizedMessage(
        id=generate_message_id(),
        tenant_id=tenant_id,
        platform=platform,
        source_id=msg_data.get("mid", str(entry.get("id", ""))),
        sender_id=sender.get("id", "unknown"),
        sender_name=None,
        content=msg_data.get("text", ""),
        content_type="text" if "text" in msg_data else "attachment",
        metadata={"entry_id": entry.get("id"), "timestamp": entry.get("time")},
        received_at=datetime.utcnow(),
    )


def normalize_twitter_dm(tenant_id: str, event: dict) -> NormalizedMessage:
    """Normalize Twitter direct message."""
    msg_create = event.get("message_create", {})
    msg_data = msg_create.get("message_data", {})

    return NormalizedMessage(
        id=generate_message_id(),
        tenant_id=tenant_id,
        platform=PlatformType.TWITTER,
        source_id=event.get("id", ""),
        sender_id=msg_create.get("sender_id", "unknown"),
        sender_name=None,
        content=msg_data.get("text", ""),
        content_type="text",
        metadata={"created_timestamp": event.get("created_timestamp")},
        received_at=datetime.utcnow(),
    )


def normalize_app_review(
    tenant_id: str, platform: PlatformType, review: dict
) -> NormalizedMessage:
    """Normalize app store review."""
    return NormalizedMessage(
        id=generate_message_id(),
        tenant_id=tenant_id,
        platform=platform,
        source_id=review.get("id", ""),
        sender_id=review.get("author_id", review.get("reviewerNickname", "anonymous")),
        sender_name=review.get("author_name", review.get("reviewerNickname")),
        content=review.get("body", review.get("text", "")),
        content_type="rating",
        rating=review.get("rating", review.get("score")),
        metadata={
            "title": review.get("title"),
            "version": review.get("app_version", review.get("reviewerVersion")),
        },
        received_at=datetime.utcnow(),
    )
