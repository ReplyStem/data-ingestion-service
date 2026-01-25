"""
SQS Publisher.

AWS SQS implementation of the message publisher.
"""

import json
import logging

from publishers.base import BasePublisher
from schemas.normalized import NormalizedMessage
from core.config import get_settings

logger = logging.getLogger(__name__)


class SQSPublisher(BasePublisher):
    """AWS SQS message publisher."""

    def __init__(self):
        self.settings = get_settings()
        self._client = None

    async def _get_client(self):
        """Lazy initialization of SQS client."""
        if self._client is None:
            try:
                from aiobotocore.session import get_session

                session = get_session()
                self._client = await session.create_client(
                    "sqs", region_name=self.settings.AWS_REGION
                ).__aenter__()
            except Exception as e:
                logger.warning(f"SQS client init failed: {e}. Using mock mode.")
        return self._client

    async def publish(self, message: NormalizedMessage) -> bool:
        """Publish message to SQS queue."""
        if not self.settings.SQS_QUEUE_URL:
            logger.info(f"[MOCK] Published message {message.id} to queue")
            return True

        try:
            client = await self._get_client()
            if client:
                await client.send_message(
                    QueueUrl=self.settings.SQS_QUEUE_URL,
                    MessageBody=json.dumps(message.model_dump(mode="json")),
                    MessageGroupId=message.tenant_id,
                )
                logger.info(f"Published message {message.id} to SQS")
            return True
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            return False

    async def health_check(self) -> bool:
        """Check SQS connectivity."""
        if not self.settings.SQS_QUEUE_URL:
            return True  # Mock mode always healthy
        try:
            client = await self._get_client()
            return client is not None
        except Exception:
            return False
