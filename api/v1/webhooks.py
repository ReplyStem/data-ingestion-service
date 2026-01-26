"""
Webhook Endpoints.

API endpoints for receiving platform webhooks.
"""

import logging

from fastapi import APIRouter, Request, Header, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session_factory
from handlers import HandlerFactory
from normalizers import normalize_meta_message
from publishers import SQSPublisher
from repositories import MessageRepository
from schemas import MetaWebhookPayload, WebhookResponse, PlatformType

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

publisher = SQSPublisher()


async def _process_webhook(
    tenant_id: str,
    platform: PlatformType,
    payload: dict,
    credentials: dict | None = None,
) -> WebhookResponse:
    """Common webhook processing logic."""
    handler = HandlerFactory.get_webhook_handler(platform, credentials)
    messages = await handler.process(tenant_id, payload)

    async with get_session_factory()() as db:
        repo = MessageRepository(db)
        for msg in messages:
            # Check for duplicates
            existing = await repo.get_by_source_id(tenant_id, msg.source_id)
            if existing:
                logger.info(f"Duplicate message skipped: {msg.source_id}")
                continue

            await repo.create(msg)
            await publisher.publish(msg)

        await db.commit()

    return WebhookResponse(
        status="ok",
        message_id=messages[0].id if messages else None,
    )


@router.post("/meta/{tenant_id}", response_model=WebhookResponse)
async def meta_webhook(
    tenant_id: str,
    payload: MetaWebhookPayload,
    request: Request,
    x_hub_signature_256: str = Header(default=""),
):
    """Receive Meta (Facebook/Instagram) webhook events."""
    logger.info(f"Received Meta webhook for tenant {tenant_id}")

    # TODO: Fetch credentials from tenant_service
    return await _process_webhook(
        tenant_id, PlatformType.INSTAGRAM, payload.model_dump()
    )


@router.get("/meta/{tenant_id}")
async def meta_webhook_verify(
    tenant_id: str,
    hub_mode: str = Query(default="", alias="hub.mode"),
    hub_verify_token: str = Query(default="", alias="hub.verify_token"),
    hub_challenge: str = Query(default="", alias="hub.challenge"),
):
    """Meta webhook verification challenge."""
    logger.info(f"Meta verification: mode={hub_mode}, token={hub_verify_token}, challenge={hub_challenge}")
    # TODO: Verify token against tenant_service
    if hub_mode == "subscribe":
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/twitter/{tenant_id}", response_model=WebhookResponse)
async def twitter_webhook(tenant_id: str, request: Request):
    """Receive Twitter/X webhook events."""
    logger.info(f"Received Twitter webhook for tenant {tenant_id}")
    payload = await request.json()
    return await _process_webhook(tenant_id, PlatformType.TWITTER, payload)


@router.get("/twitter/{tenant_id}")
async def twitter_crc_challenge(crc_token: str, tenant_id: str):
    """Twitter CRC challenge response."""
    from handlers.webhooks.twitter import TwitterWebhookHandler

    # TODO: Fetch credentials from tenant_service
    handler = TwitterWebhookHandler(consumer_secret="")
    response_token = handler.create_crc_response(crc_token)
    return {"response_token": response_token}
