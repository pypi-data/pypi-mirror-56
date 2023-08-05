"""Common logic/settings of Stream-RPC server/client."""
import os
import asyncio
import logging
import uuid

from abc import ABC, abstractmethod
from collections import namedtuple
from datetime import datetime

from stream_rpc.crypto import Cypher

STREAM_RPC_HOST = os.getenv("STREAM_RPC_HOST", "0.0.0.0")
STREAM_RPC_PORT = int(os.getenv("STREAM_RPC_HOST", "8888"))
STREAM_RPC_TERM = b"\n"
STREAM_RPC_CYPHER = Cypher
STREAM_RPC_LOG_LVL = getattr(logging, os.getenv("STREAM_RPC_LOG_LVL", "INFO"))
STREAM_RPC_LOG_FMT = (
    "%(asctime)-15s %(name)-5s\n  \\_ %(levelname)-8s %(message)s"
)

logging.basicConfig(format=STREAM_RPC_LOG_FMT, level=STREAM_RPC_LOG_LVL)

MessagePacket = namedtuple(
    "MessagePacket",
    ["peer", "id", "created_at", "method", "payload"],
    defaults=[{}],
)


class StreamRPCAdapter(logging.LoggerAdapter):
    """Extend basic log record by protocol specific data."""

    def process(self, msg, kwargs):
        """Process log record."""
        return (
            "[%s] %s" % (self.extra["peer"], msg),
            kwargs,
        )


def create_message_packet(peer_id, request_number, method, payload=None):
    """Create message packet, see :py:class:`MessagePacket` above.

    :param peer_id: peer id
    :param int request_number: number of reuest
    :param str method: RPC method
    :param payload: any pickled data

    """
    if not payload:
        payload = {}
    return MessagePacket(
        peer=peer_id,
        id=request_number,
        created_at=datetime.utcnow(),
        method=method,
        payload=payload,
    )


class Protocol(ABC):
    """An abstract base class for Server/Client protocol classes.

    You should not use this class directly, you should create a new ones
    (client/server) classes inherited from this and define in them the
    `process_message` method.
    """

    def __init__(
        self,
        peer_id,
        reader,
        writer,
        message_separator=STREAM_RPC_TERM,
        cypher=STREAM_RPC_CYPHER,
    ):
        """Initialize class.

        :param str peer_id: id of peer
        :param asyncio.StreamReader reader: interface for reading from stream
        :param asyncio.StreamWriter writer: interface for writing to stream
        :param message_separator:
        :param cypher:


        """
        self.cypher = cypher()
        self.reader = reader
        self.writer = writer
        self.peer_id = peer_id
        self.request_number = 1
        self.message_separator = message_separator
        self.logger = StreamRPCAdapter(
            logging.getLogger(self.__class__.__name__), {"peer": self.peer_id},
        )

    def create_message_packet(self, *args, **kwargs):
        """Create message packet using helper function defined above."""
        return create_message_packet(
            self.peer_id, self.request_number, *args, **kwargs
        )

    def msg_encrypt(self, msg):
        """Encrypt message.

        :param msg: any pickled data
        :returns: encypted message
        :rtype: bytes

        """
        return self.cypher.encrypt(msg)

    def msg_decrypt(self, msg):
        """Decrypt message.

        :param msg: previously encrypted message by `self.msg_encrypt()`
        :returns: origin message

        """
        return self.cypher.decrypt(msg)

    def encrypt_message_packet(self, message_packet):
        """Encrypt message packet.

        :param MessagePacket message_packet: a message packet

        """
        packet = self.msg_encrypt(message_packet)
        packet += self.message_separator
        return packet

    async def send_message(self, message_packet):
        """Send a message.

        Sending message to another side will expect response, which will be
        processed in self.process_message(), so after every sending
        self.read_message() will be execute.

        :param message_packet: a message packet

        """
        self.logger.info("Send: %s", message_packet)

        encrypted_message_packet = self.encrypt_message_packet(message_packet)

        try:
            self.writer.write(encrypted_message_packet)
            await self.writer.drain()
        except Exception as er:
            self.writer.close()
            self.logger.error("Network problems: %s", er)
            return
        else:
            self.request_number += 1

        await self.read_message()

    async def read_message(self):
        """Read message.

        Reading message from another side involves execution of
        `self.process_message()`, you chould not change this method,
        you should define all you needed in `process_message()`.

        """
        try:
            encrypted_message_packet = await self.reader.readuntil(
                self.message_separator
            )
        except Exception as er:
            self.logger.error("Read incomplete, %s", er)
            return

        message_packet = self.msg_decrypt(encrypted_message_packet)

        self.logger.info("Received: %s", message_packet)

        await self.process_message(message_packet)

    @abstractmethod
    async def process_message(self, message_packet):
        """Child class must define this method.

        Define in child class client/server logic of processing
        incoming data.

        :param MessagePacket message_packet: a message packet

        """
        ...


class Connector:
    """Connector of client-server sides.

    The purpose of this class is to keep the transport layer data(server
    address and port).
    """

    def __init__(
        self,
        protocol_class,
        stream_rpc_host=STREAM_RPC_HOST,
        stream_rpc_port=STREAM_RPC_PORT,
    ):
        """Initialize class.

        :param protocol_class: a protocol class
        :param str stream_rpc_host: Stream-RPC server address for connections
        :param int stream_rpc_port: Stream-RPC port for connections

        """
        self.protocol_class = protocol_class
        self.stream_rpc_host = stream_rpc_host
        self.stream_rpc_port = stream_rpc_port
        self.peer_id = str(uuid.uuid1())
        self.logger = StreamRPCAdapter(
            logging.getLogger(self.__class__.__name__), {"peer": self.peer_id}
        )

    async def process_incoming_connection(self, reader, writer):
        """Process incoming connection, callback of `asyncio.start_server()`.

        :param asyncio.StreamReader reader: interface for reading from stream
        :param asyncio.StreamWriter writer: interface for writing to stream
        :returns: None
        :rtype: NoneType

        """
        server = self.protocol_class(self.peer_id, reader, writer)
        await server.read_message()

    async def run_server(self):
        """Run server."""
        server = await asyncio.start_server(
            self.process_incoming_connection,
            self.stream_rpc_host,
            self.stream_rpc_port,
        )

        addr = server.sockets[0].getsockname()
        self.logger.info("Start Stream-RPC server, listen on %s:%s", *addr)

        async with server:
            await server.serve_forever()

    async def run_client(self, hello_message):
        """Run client.

        :param `stream_rpc.common.MessagePacket` hello_message: a hello message,
        which client will send at the time of first connection.

        """
        reader, writer = await asyncio.open_connection(
            self.stream_rpc_host, self.stream_rpc_port
        )
        client = self.protocol_class(self.peer_id, reader, writer)

        await client.send_message(hello_message)
        client.writer.close()
        await writer.wait_closed()
