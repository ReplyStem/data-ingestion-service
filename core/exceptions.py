"""
Custom Exceptions.

Application-specific exceptions for error handling.
"""

from fastapi import HTTPException, status


class IngestionException(Exception):
    """Base exception for ingestion service."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class WebhookValidationError(IngestionException):
    """Raised when webhook signature validation fails."""

    pass


class PlatformNotConfiguredError(IngestionException):
    """Raised when platform is not configured for tenant."""

    pass


class TenantServiceError(IngestionException):
    """Raised when tenant service call fails."""

    pass


def not_found(detail: str = "Resource not found") -> HTTPException:
    """Return a 404 HTTPException."""
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def bad_request(detail: str = "Bad request") -> HTTPException:
    """Return a 400 HTTPException."""
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
