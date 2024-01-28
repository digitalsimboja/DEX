"""DEX Exchange Base"""
import asyncio
import logging
from logging import Logger
from typing import Optional

from api.dex_exchange_base import DEXExchangeBase
from api.hyperliquid.constants import PATH_TO_HYPERLIQUID
from caching.stream_manager import RedisStreamManager
from caching.streams import StreamNameBuilder
from models.enums import Blockchains, DataType, Exchanges, StreamNames
from requests import Response
from utilities.config import get_config


_PATH_TO_REDIS_CONFIG = PATH_TO_HYPERLIQUID / "redis_config.json"
_redis_stream_manager = RedisStreamManager.from_config(_PATH_TO_REDIS_CONFIG)

_stream_name_builder = (
    StreamNameBuilder()
    .set("marketplace", Exchanges.HYPERLIQUID)
    .set("blockchain", Blockchains.COSMOS)
    .set("data_type", DataType.RAW)
)
_REDIS_STREAMS = {
    stream: _stream_name_builder.set("stream", stream).name for stream in StreamNames
}


class HyperLiquid(DEXExchangeBase):
    """
    Base DEX Exchange Instance

    When we need to execute specifically against DEX Marketplaces,
    utilize this object to standardize the required properties and
    methods to interact with said counterparties.
    """

    _confi_data = get_config()
    _hyperliquid_config = _confi_data["hyperliquid"]

    def __init__(self, logger: logging.Logger):
        super().__init__(
            api_key=self._confi_data["api_key"],
            api_qps=self._confi_data["api_qps"],
            logger=logger
        )
        self._base_rest_url = self._hyperliquid_config["base_url"]
        self._base_websocket_url = self._hyperliquid_config["websocket_url"]
        self._rest_endpoint_urls = self._hyperliquid_config["endpoints"]

    @property
    def base_rest_url(self) -> str:
        return self._base_rest_url

    @property
    def base_websocket_url(self) -> str:
        return self._base_websocket_url

    @property
    def rest_endpoint_urls(self) -> dict[str, str]:
        return self._rest_endpoint_urls

    @property
    def session_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    @_redis_stream_manager.publish_result(_REDIS_STREAMS[StreamNames.PRICES])
    async def get_all_mids(self) -> Response:
        url = self.get_rest_endpoint_url("allMids")
        body = {
            "type": "allMids"
        }
        try:
            response = self.session.post(url=url, json=body)
            response.raise_for_status() 
            print("Response status code:", response.status_code)
            print("Response data:", response.json())
            return response
        except Exception as e:
            print("Error in retrieving all mids:", e)
            return None 
