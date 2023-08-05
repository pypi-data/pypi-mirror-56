import json

import aiojobs
import aio_pika
from aio_pika.patterns import RPC

from typing import Callable, Awaitable


class JsonRPC(RPC):
    SERIALIZER = json
    CONTENT_TYPE = 'application/json'

    def serialize(self, data) -> bytes:
        return self.SERIALIZER.dumps(data, ensure_ascii=False, default=repr).encode()

    def serialize_exception(self, exception: Exception) -> bytes:
        return self.serialize({
            "error": {
                "type": exception.__class__.__name__,
                "message": repr(exception),
                "args": exception.args,
            }
        })



class Broker(object):
    """
    On RPC errors return:
    ```python
    return self.serialize({
            "error": {
                "type": exception.__class__.__name__,
                "message": repr(exception),
                "args": exception.args,
            }
        })
    ```
    """
    def __init__(self) -> None:
        self._connection = None
        self.scheduler = None
        self._rpc_functions = dict()
        self._rpc_call_channel = None
        self._rpc_client = None
        self._rpc_server_channel = None
        self._rpc_server = None
        self._event_consumer_channel = None
        self._event_publisher_channel = None
        self._direct_consumer_channel = None
        self._direct_publisher_channel = None
        self._exchanges = dict()

    def add_rpc_func(self, name, func):
        self._rpc_functions[name] = func
        
    async def register_rpc_functions(self):
        for name, func in self._rpc_functions.items():
            await self.register_rpc_function(name, func)
            
    async def init_event_decorators(self):
        self.scheduler = await aiojobs.create_scheduler()

    async def close(self):
        await self._connection.close()
        
    def add_close_callback(self, *args, **kwargs):
        self._connection.add_close_callback(*args, **kwargs)
    
    def add_reconnect_callback(self, *args, **kwargs):
        self._connection.add_reconnect_callback(*args, **kwargs)

    @property
    def connection(self) -> aio_pika.connection.Connection:
        return self._connection

    async def connect(self, *args, **kwargs) -> None:
        self._connection = await aio_pika.connect_robust(*args, **kwargs)
    
    async def get_rpc_client(self):
        """
        Get or create RPC client
        """
        if self._rpc_call_channel is None:
            self._rpc_call_channel = await self._connection.channel()
            if self._rpc_client is None:
                self._rpc_client = await JsonRPC.create(self._rpc_call_channel)
                return self._rpc_client
            await self._rpc_client.initialize()
        elif self._rpc_client is None:
            self._rpc_client = await JsonRPC.create(self._rpc_call_channel)
            return self._rpc_client
        return self._rpc_client
    
    def is_registered(self, func):
        return self._rpc_server and func in self._rpc_server.consumer_tags
    
    # async def register_rpc_function(self, name: str, function: Callable[[...], Awaitable[...]]) -> None:
    async def register_rpc_function(self, name: str, function) -> None:
        if self._rpc_server is None:
            if self._rpc_server_channel is None:
                self._rpc_server_channel = await self._connection.channel()
            self._rpc_server = await JsonRPC.create(self._rpc_server_channel)
        await self._rpc_server.register(name, function, auto_delete=False)
    
    async def publish_event(self,
                            exchange_name: str,
                            routing_key: str,
                            data: dict,
                            durable: bool = True,
                            content_type: str = 'application/json',
                            content_encoding: str = 'utf-8') -> None:
        if self._event_publisher_channel is None:
            self._event_publisher_channel = await self._connection.channel()
        if exchange_name in self._exchanges:
            exchange = self._exchanges[exchange_name]
        else:
            exchange = await self._event_publisher_channel.declare_exchange(
                name=exchange_name,
                type=aio_pika.ExchangeType.TOPIC,
                durable=durable,
                auto_delete=False,
                internal=False,
                passive=False
            )
            self._exchanges[exchange_name] = exchange
        message = aio_pika.Message(
            body=json.dumps(data).encode(),
            content_type=content_type,
            content_encoding=content_encoding,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        await exchange.publish(
            message,
            routing_key=routing_key
        )
    
    async def register_event_consumer(self,
                                      exchange_name: str,
                                      queue_name: str,
                                      routing_key: str,
                                      callback,
                                      durable: bool = True,
                                      no_ack: bool = False) -> None:
        if self._event_consumer_channel is None:
            self._event_consumer_channel = await self._connection.channel()
        exchange = await self._event_consumer_channel.declare_exchange(
            name=exchange_name,
            type=aio_pika.ExchangeType.TOPIC,
            durable=durable,
            auto_delete=False,
            internal=False,
            passive=False
        )
        queue = await self._event_consumer_channel.declare_queue(
            name=queue_name,
            durable=durable,
            exclusive=False,
            passive=False,
            auto_delete=False
        )
        await queue.bind(exchange, routing_key=routing_key)
        await queue.consume(
            callback=callback,
            no_ack=no_ack,
            exclusive=False,
        )
        
    async def publish_direct(self,
                            exchange_name: str,
                            direct: str,
                            data: dict,
                            durable: bool = True,
                            content_type: str = 'application/json',
                            content_encoding: str = 'utf-8') -> None:
        if self._direct_publisher_channel is None:
            self._direct_publisher_channel = await self._connection.channel()
        if exchange_name in self._exchanges:
            exchange = self._exchanges[exchange_name]
        else:
            exchange = await self._direct_publisher_channel.declare_exchange(
                name=exchange_name,
                type=aio_pika.ExchangeType.DIRECT,
                durable=durable,
                auto_delete=False,
                internal=False,
                passive=False
            )
            self._exchanges[exchange_name] = exchange
        message = aio_pika.Message(
            body=json.dumps(data).encode(),
            content_type=content_type,
            content_encoding=content_encoding,
            delivery_mode=aio_pika.DeliveryMode.NOT_PERSISTENT,
        )
        await exchange.publish(
            message,
            routing_key=direct
        )
    
    async def register_direct_consumer(self,
                                      exchange_name: str,
                                      queue_name: str,
                                      direct: str,
                                      callback,
                                      durable: bool = True,
                                      no_ack: bool = True) -> None:
        if self._direct_consumer_channel is None:
            self._direct_consumer_channel = await self._connection.channel()
        exchange = await self._direct_consumer_channel.declare_exchange(
            name=exchange_name,
            type=aio_pika.ExchangeType.DIRECT,
            durable=durable,
            auto_delete=False,
            internal=False,
            passive=False
        )
        queue = await self._event_consumer_channel.declare_queue(
            name=queue_name,
            durable=durable,
            exclusive=False,
            passive=False,
            auto_delete=False
        )
        await queue.bind(exchange, routing_key=direct)
        await queue.consume(
            callback=callback,
            no_ack=no_ack,
            exclusive=False,
        )
