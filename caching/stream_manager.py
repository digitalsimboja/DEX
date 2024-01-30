import json
from functools import wraps
from pathlib import Path
from typing import Callable, Type

from pydantic import BaseModel
from redis.asyncio import Redis, ResponseError
from redis.asyncio.connection import ConnectionPool
from utilities.parsing import JsonParser
from utilities.logger import SetupLogger

_MAX_JSON_LEN = 10_000


class RedisStreamManager(Redis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger_config = SetupLogger(
            'redis_stream', 'logs/redis_stream_manager.log')
        self.logger = self.logger_config.create_logger()

    @classmethod
    def from_config(cls, json_config_file_path: Path) -> Redis:
        """
        Implement our extension of the async redis client using values from a json config

        json_config_file_path:
        """
        with open(json_config_file_path, "rb") as f:
            configs = json.load(f)
        redis_url = f"redis://{configs['host']}:{configs['port']}/{configs['db']}"
        # connection_pool = ConnectionPool.from_url(**configs)
        connection_pool = ConnectionPool.from_url(redis_url)
        client = cls(
            connection_pool=connection_pool,
            single_connection_client=False,
        )
        client.auto_close_connection_pool = True
        return client

    def publish_result(
        self,
        stream_name: str,
        message_model: Type[BaseModel] | None = None,
    ) -> Callable:
        """
        Decorator generator for async functions that will publish results to redis

        :param stream_name:
        :param message_model:
        :return: the wrapper to send output into redis
        """

        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Call the original function and get the result
                result = await func(*args, **kwargs)

                # Convert the generic value into a json string
                json_result = JsonParser.loads(result)
                self.logger.debug(
                    "Received the data %s for the stream  %s and publishing to redis ", json_result, stream_name)

                # Publish the message to the specified Redis stream
                await self.xadd(
                    stream_name,
                    json.loads(json_result),
                    maxlen=_MAX_JSON_LEN,
                    approximate=True,
                )

                return result

            return wrapper

        return decorator

    async def create_redis_consumer_group(self, stream_name: str, group_name: str):
        """
        Asynchronously creates a consumer group for a given stream in Redis.
        """
        try:
            self.logger.debug(
                'Creating the consumer group with stream name %s with group name %s ', stream_name, group_name)
            await self.xgroup_create(stream_name, group_name, id="0")
        except ResponseError as e:
            if "BUSYGROUP Consumer Group name already exists" not in str(e):
                raise
