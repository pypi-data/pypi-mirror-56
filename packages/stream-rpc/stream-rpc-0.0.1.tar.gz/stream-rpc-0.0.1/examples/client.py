"""Stream-RPC client."""
import asyncio
import random
from stream_rpc.common import Protocol, Connector, create_message_packet


class ClientProtocol(Protocol):
    """A RPC client."""

    sleep_time = 2

    async def process_message(self, message_packet):
        """Process payload of message."""
        message = self.create_message_packet("ping")

        method = message_packet.method
        payload = message_packet.payload

        if method == "parse_article":
            self.logger.info("Start parsing article: %s", payload)
            await asyncio.sleep(5)

        if self.request_number % 2 == 0:
            task = self.create_message_packet(
                "parse_article", {"article_id": random.randint(1000, 10000)}
            )
            message = self.create_message_packet("put_in_queue", task)
        elif self.request_number % 5 == 0:
            message = self.create_message_packet("get_task_from_queue")

        if self.sleep_time:
            self.logger.info(f"Sleep for {self.sleep_time} seconds...")

        await asyncio.sleep(self.sleep_time)
        await self.send_message(message)


if __name__ == "__main__":
    connector = Connector(ClientProtocol)
    message = create_message_packet(connector.peer_id, 1, "ping")
    try:
        asyncio.run(connector.run_client(message))
    except KeyboardInterrupt:
        connector.logger.warning('connector unplugged')
        exit
    except (ConnectionRefusedError, BrokenPipeError):
        connector.logger.warning('server is unreachable')
        exit
