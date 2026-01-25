"""
Application Configuration.

Loads all settings from environment variables using Pydantic.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Server
    API_HOST: str = Field(default="0.0.0.0", description="API server host")
    API_PORT: int = Field(default=8002, description="API server port")

    # Database
    DATABASE_URL: str = Field(
        ..., description="PostgreSQL connection string (use postgresql+asyncpg://)"
    )

    # Tenant Service
    TENANT_SERVICE_URL: str = Field(
        default="http://localhost:8001",
        description="Tenant service base URL for secrets",
    )

    # Message Queue
    SQS_QUEUE_URL: str = Field(
        default="", description="SQS queue URL for publishing messages"
    )
    AWS_REGION: str = Field(default="us-east-1", description="AWS region")

    # Workers
    WORKER_POLL_INTERVAL: int = Field(
        default=900, description="Polling interval in seconds (default 15 min)"
    )

    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
