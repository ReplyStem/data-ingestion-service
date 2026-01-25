"""
Data Ingestion Service - Main Entry Point.

FastAPI application for ingesting data from multiple platforms.
"""

import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from core.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("data_ingestion_service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("=" * 60)
    logger.info("Data Ingestion Service Starting")
    logger.info("=" * 60)
    yield
    logger.info("Data Ingestion Service Shutting Down")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Data Ingestion Service",
        description="Ingests data from webhooks and polling sources.",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.include_router(api_router)

    @app.get("/health", tags=["Health"])
    async def root_health():
        return {"status": "healthy", "service": "data-ingestion-service"}

    return app


app = create_app()


def main():
    """Run the server."""
    settings = get_settings()
    logger.info(f"Starting server on {settings.API_HOST}:{settings.API_PORT}")
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
