"""Stream-RPC server."""
import asyncio
from collections import deque
from stream_rpc.common import Protocol, Connector

queue = deque()


class ServerProtocol(Protocol):
    """A RPC server."""

    async def process_message(self, message_packet):
        """Process payload of message."""
        message = self.create_message_packet("pong")

        payload = message_packet.payload
        method = message_packet.method

        # self.logger.info("Process payload: %s", payload)

        if method == "ping":
            await self.send_message(message)
        elif method == "put_in_queue":
            queue.append(payload)
        elif method == "get_task_from_queue":
            try:
                task_data = queue.pop()
            except IndexError:
                # INFO: there are no tasks
                pass
            else:
                message = task_data

        await self.send_message(message)


if __name__ == "__main__":
    connector = Connector(ServerProtocol)
    try:
        asyncio.run(connector.run_server())
    except KeyboardInterrupt:
        connector.logger.warning('connector unplugged')
        exit
