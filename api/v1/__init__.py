"""API v1 router."""

from fastapi import APIRouter

from api.v1.health import router as health_router
from api.v1.webhooks import router as webhooks_router

router = APIRouter(prefix="/api/v1")
router.include_router(health_router)
router.include_router(webhooks_router)

__all__ = ["router"]
