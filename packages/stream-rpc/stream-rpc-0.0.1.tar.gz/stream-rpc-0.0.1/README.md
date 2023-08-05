# Overview

Stream RPC it is the primitive RPC protocol with the cryptography included:
all messages will be encrypted. It is not traditional RPC protocol,
it looks like abstract protocol of peer-to-peer messages, which you
can use for your particular cases.

## Package structure

There are two modules: `common` and `crypto`. The `common` contains common for clien/server
interfaces (classes), helper functions etc. The `crypto` contains the `Cypher` class,
which should define two functions: `encrypt` and `decrypt`, you can override them
or even whole class.

The `stream_rpc.common` module provides classes:
 - `Protocol` it is abstract class for creation your own classes: `ServerProtocol`
    and `ClientProtocol`, typically you should define only `process_message` method.
 - `Connector` it is class for run client/server: server will listen on particular
   address and port (settings will be pulled from os environ variables) and client
   will connect to special host:port

and helper function:
 - `create_message_packet` used for manual creation of Stream RPC Message Packet,
   basically you will use it only for sending "hello" message in startup phase (later
   this function will be removed)

## Configurable settings

Settings which you can override through OS environment variables:

 - `CRYPTO_KEY` password which will use for encryption/decryption of messages
 - `STREAM_RPC_HOST` host address on which server will listen for incoming connections and
   client will connect, default: 0.0.0.0 (all system network interfaces)
 - `STREAM_RPC_PORT` a port number on which server will listen for incoming connections and
   client will connect, default: 8888
 - `STREAM_RPC_LOG_LVL` log level, default: INFO

Settings which you should override in your code:

 - `STREAM_RPC_TERM` separator of messages in stream, default: b"\n"
 - `STREAM_RPC_CYPHER` cypher which will use for encryption/decryption of messages,
   default: `stream_rpc.crypto.Cypher`
 - `STREAM_RPC_LOG_FMT` format of log messages

# Examples of usage

## Define a server

Start from server definition, you should think about what the server will do with
incoming data? What are methods your RPC server will be accept,
what actions should be done etc. For simplification example let's assume that
our RPC server will accept 3 methods:
 - `ping`, server will respond `pong`
 - `put_in_queue`, server will put the incoming message into queue and then a client
   somewhen get this task back for processing, server will respond `pong`
 - `get_task_from_queue`, server get one task back from queue and send it to client,
   we will not modify task data, just send original saved message packet

So the code of ServerProtocol would be look like this:

```python
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

```

Ok, it is cool: our server will not know nothing about tasks,
it just save some task in queue and then get and send it back by the client request.
It is very flexible.

## Define a client

When you think about "client" you should think about it as about "worker",
in fact it will be doing all work. Let's assume we want to parse the big blogging platform
and want to distribute this tasks of parsing across our available servers or
micro cloud instances. For simplification, let's assume that our client will put a new task
with every second request and will ask the server about a new task (which might created
by another one client) for parsing on every fifth request. Then our `ClientProtocol`
would be look like this:

```python
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
            # INFO: here is the parsing and create a message packet with parsed data
            # in this example we use a sleep for simulate a long time process...
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

```

Ok, looks fine: we have full control about what our distributed system will do.

Of course, in this example a big part of code is missed:
 - Where server will be store parsed data?
 - What method will be used for that? `save_parsed_article`?
 - How-to prevent duplicates of tasks?
 - etc..

It was deliberately omitted it so as not to make the example a very large.

But, in fact, we already defined server and client, let's run them!


## Prepare environ and run client/server

Let's create a strong password which `stream_rpc` will used for encryption its messages.

```
 $ python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key())"
b'EDCxyWkoWp9HjjXhaObi4PoORMUTIiZ4jIWAAKLUvgs='
```

Ok, set up the environ variable `CRYPTO_KEY` and run `server.py` (see the `examples` folder):

```
$ export CRYPTO_KEY=EDCxyWkoWp9HjjXhaObi4PoORMUTIiZ4jIWAAKLUvgs=

$ export STREAM_RPC_HOST=127.0.0.1

$ export STREAM_RPC_HOST=8899

$ python server.py
2019-11-19 20:49:11,244 Connector
  \_ INFO     [e4a384f8-0af4-11ea-8e6d-a08869d09fd5] Start Stream-RPC server, listen on 127.0.0.1:8899
2019-11-19 20:49:26,449 ServerProtocol
  \_ INFO     [e4a384f8-0af4-11ea-8e6d-a08869d09fd5] Received: MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=1, created_at=datetime.datetime(2019, 11, 19, 17, 49, 26, 401400), method='ping', payload={})
2019-11-19 20:49:26,450 ServerProtocol
  \_ INFO     [e4a384f8-0af4-11ea-8e6d-a08869d09fd5] Send: MessagePacket(peer='e4a384f8-0af4-11ea-8e6d-a08869d09fd5', id=1, created_at=datetime.datetime(2019, 11, 19, 17, 49, 26, 450014), method='pong', payload={})
2019-11-19 20:49:28,454 ServerProtocol
  \_ INFO     [e4a384f8-0af4-11ea-8e6d-a08869d09fd5] Received: MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=2, created_at=datetime.datetime(2019, 11, 19, 17, 49, 26, 451001), method='put_in_queue', payload=MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=2, created_at=datetime.datetime(2019, 11, 19, 17, 49, 26, 450996), method='parse_article', payload={'article_id': 3520}))
2019-11-19 20:49:28,454 ServerProtocol
  \_ INFO     [e4a384f8-0af4-11ea-8e6d-a08869d09fd5] Send: MessagePacket(peer='e4a384f8-0af4-11ea-8e6d-a08869d09fd5', id=2, created_at=datetime.datetime(2019, 11, 19, 17, 49, 28, 454676), method='pong', payload={})
2019-11-19 20:49:30,461 ServerProtocol
  \_ INFO     [e4a384f8-0af4-11ea-8e6d-a08869d09fd5] Received: MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=3, created_at=datetime.datetime(2019, 11, 19, 17, 49, 28, 456569), method='ping', payload={})
2019-11-19 20:49:30,461 ServerProtocol
  \_ INFO     [e4a384f8-0af4-11ea-8e6d-a08869d09fd5] Send: MessagePacket(peer='e4a384f8-0af4-11ea-8e6d-a08869d09fd5', id=3, created_at=datetime.datetime(2019, 11, 19, 17, 49, 30, 461638), method='pong', payload={})
2019-11-19 20:49:32,468 ServerProtocol
  \_ INFO     [e4a384f8-0af4-11ea-8e6d-a08869d09fd5] Received: MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=4, created_at=datetime.datetime(2019, 11, 19, 17, 49, 30, 463686), method='put_in_queue', payload=MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=4, created_at=datetime.datetime(2019, 11, 19, 17, 49, 30, 463671), method='parse_article', payload={'article_id': 3249}))
2019-11-19 20:49:32,469 ServerProtocol
  \_ INFO     [e4a384f8-0af4-11ea-8e6d-a08869d09fd5] Send: MessagePacket(peer='e4a384f8-0af4-11ea-8e6d-a08869d09fd5', id=4, created_at=datetime.datetime(2019, 11, 19, 17, 49, 32, 469208), method='pong', payload={})
2019-11-19 20:49:34,476 ServerProtocol
  \_ INFO     [e4a384f8-0af4-11ea-8e6d-a08869d09fd5] Received: MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=5, created_at=datetime.datetime(2019, 11, 19, 17, 49, 32, 471254), method='get_task_from_queue', payload={})
2019-11-19 20:49:34,476 ServerProtocol
  \_ INFO     [e4a384f8-0af4-11ea-8e6d-a08869d09fd5] Send: MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=4, created_at=datetime.datetime(2019, 11, 19, 17, 49, 30, 463671), method='parse_article', payload={'article_id': 3249})
2019-11-19 20:49:41,489 ServerProtocol
  \_ INFO     [e4a384f8-0af4-11ea-8e6d-a08869d09fd5] Received: MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=6, created_at=datetime.datetime(2019, 11, 19, 17, 49, 39, 484574), method='put_in_queue', payload=MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=6, created_at=datetime.datetime(2019, 11, 19, 17, 49, 39, 484553), method='parse_article', payload={'article_id': 7917}))
2019-11-19 20:49:41,489 ServerProtocol
  \_ INFO     [e4a384f8-0af4-11ea-8e6d-a08869d09fd5] Send: MessagePacket(peer='e4a384f8-0af4-11ea-8e6d-a08869d09fd5', id=6, created_at=datetime.datetime(2019, 11, 19, 17, 49, 41, 489694), method='pong', payload={})
```

and run `client.py`:

```
$ export CRYPTO_KEY=EDCxyWkoWp9HjjXhaObi4PoORMUTIiZ4jIWAAKLUvgs=

$ export STREAM_RPC_HOST=127.0.0.1

$ export STREAM_RPC_HOST=8899

$ python client.py
2019-11-19 20:49:26,447 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Send: MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=1, created_at=datetime.datetime(2019, 11, 19, 17, 49, 26, 401400), method='ping', payload={})
2019-11-19 20:49:26,450 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Received: MessagePacket(peer='e4a384f8-0af4-11ea-8e6d-a08869d09fd5', id=1, created_at=datetime.datetime(2019, 11, 19, 17, 49, 26, 450014), method='pong', payload={})
2019-11-19 20:49:26,451 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Sleep for 2 seconds...
2019-11-19 20:49:28,452 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Send: MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=2, created_at=datetime.datetime(2019, 11, 19, 17, 49, 26, 451001), method='put_in_queue', payload=MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=2, created_at=datetime.datetime(2019, 11, 19, 17, 49, 26, 450996), method='parse_article', payload={'article_id': 3520}))
2019-11-19 20:49:28,456 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Received: MessagePacket(peer='e4a384f8-0af4-11ea-8e6d-a08869d09fd5', id=2, created_at=datetime.datetime(2019, 11, 19, 17, 49, 28, 454676), method='pong', payload={})
2019-11-19 20:49:28,456 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Sleep for 2 seconds...
2019-11-19 20:49:30,459 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Send: MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=3, created_at=datetime.datetime(2019, 11, 19, 17, 49, 28, 456569), method='ping', payload={})
2019-11-19 20:49:30,463 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Received: MessagePacket(peer='e4a384f8-0af4-11ea-8e6d-a08869d09fd5', id=3, created_at=datetime.datetime(2019, 11, 19, 17, 49, 30, 461638), method='pong', payload={})
2019-11-19 20:49:30,463 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Sleep for 2 seconds...
2019-11-19 20:49:32,466 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Send: MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=4, created_at=datetime.datetime(2019, 11, 19, 17, 49, 30, 463686), method='put_in_queue', payload=MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=4, created_at=datetime.datetime(2019, 11, 19, 17, 49, 30, 463671), method='parse_article', payload={'article_id': 3249}))
2019-11-19 20:49:32,470 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Received: MessagePacket(peer='e4a384f8-0af4-11ea-8e6d-a08869d09fd5', id=4, created_at=datetime.datetime(2019, 11, 19, 17, 49, 32, 469208), method='pong', payload={})
2019-11-19 20:49:32,471 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Sleep for 2 seconds...
2019-11-19 20:49:34,474 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Send: MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=5, created_at=datetime.datetime(2019, 11, 19, 17, 49, 32, 471254), method='get_task_from_queue', payload={})
2019-11-19 20:49:34,478 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Received: MessagePacket(peer='edac5516-0af4-11ea-82cb-a08869d09fd5', id=4, created_at=datetime.datetime(2019, 11, 19, 17, 49, 30, 463671), method='parse_article', payload={'article_id': 3249})
2019-11-19 20:49:34,478 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Start parsing article: {'article_id': 3249}
2019-11-19 20:49:39,484 ClientProtocol
  \_ INFO     [edac5516-0af4-11ea-82cb-a08869d09fd5] Sleep for 2 seconds...
```

Ok, all it's working as desired: on every second request the client will put
a new one task (parse article) into server queue and on every fifth request,
client will ask server about a task for parsing article.
