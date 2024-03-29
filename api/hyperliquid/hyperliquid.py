"""DEX Exchange Base"""
import asyncio
import logging
from typing import Optional
import json
import os
from typing import Dict

from api.dex_exchange_base import DEXExchangeBase
from api.hyperliquid.constants import PATH_TO_HYPERLIQUID
from caching.stream_manager import RedisStreamManager
from caching.streams import StreamNameBuilder
from models.enums import Blockchains, DataType, Exchanges, StreamNames
from requests import Response
from utilities.common import get_config
from utilities.parsing import JsonParser
from utilities.logger import SetupLogger


_PATH_TO_REDIS_CONFIG = PATH_TO_HYPERLIQUID / "redis_config.json"
_PATH_TO_HYPERLIQUID_CONFIG = PATH_TO_HYPERLIQUID / "hyperliquid_config.json"
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

    def __init__(self):
        self._logger_config = SetupLogger(
            'hyperliquid_api', 'logs/hyperliquid/hyperliquid_api.log')
        self._hyperliquid_logger = self._logger_config.create_logger()
        self._hyperliquid_config = self.load_config()
        self._base_rest_url = self._hyperliquid_config["base_url"]
        self._base_websocket_url = self._hyperliquid_config["websocket_url"]
        self._rest_endpoint_urls = self._hyperliquid_config["endpoints"]

        super().__init__(
            api_key=self._confi_data["api_key"], api_qps=self._confi_data["api_qps"], logger=self._hyperliquid_logger)

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

    @staticmethod
    def load_config() -> Dict:
        """
        Load the HyperLiquid-specific configuration from the 'hyperliquid_config.json' file.

        Returns:
            dict: A dictionary containing the configuration data.

        Raises:
            FileNotFoundError: If the 'hyperliquid_config.json' file is not found.
            json.JSONDecodeError: If the file does not contain valid JSON data.
        """
        hyperliquid_config_path = _PATH_TO_HYPERLIQUID_CONFIG
        with open(hyperliquid_config_path, "r") as config_file:
            return json.load(config_file)

    @_redis_stream_manager.publish_result(_REDIS_STREAMS[StreamNames.PRICES])
    async def get_all_mids(self) -> Response:
        url = self.get_rest_endpoint_url("allMids")
        body = {
            "type": "allMids"
        }
        try:
            response = self.session.post(url=url, json=body)
            response.raise_for_status()
            json_result = JsonParser.loads(response)
            self.logger.debug("Response from get_all_mids: %s", json_result)
            return json_result
        except Exception as e:
            self.logger.error("Error in retrieving all mids", exc_info=True)
            return None
