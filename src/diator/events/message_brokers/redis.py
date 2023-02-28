import logging
import redis.asyncio as redis

from diator.events.message_brokers.protocol import Message


logger = logging.getLogger(__name__)


class RedisMessageBroker:
    def __init__(
        self, client: redis.Redis, *, channel_prefix: str | None = None
    ) -> None:
        self._client = client
        self._channel_prefix = channel_prefix or "python_diator_channel"

    async def send_message(self, message: Message) -> None:
        async with self._client.pubsub() as pubsub:
            channel = f"{self._channel_prefix}:{message.message_id}"

            await pubsub.subscribe(channel)

            logger.info("Sending event to Redis Pub/Sub %s.", message.message_id)
            await self._client.publish(channel, message.payload)
