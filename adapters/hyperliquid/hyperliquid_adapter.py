import asyncio
from adapters.dex_adapter_base import RawDataAdapter
from api.hyperliquid.constants import PATH_TO_HYPERLIQUID
from caching.stream_manager import RedisStreamManager
from caching.streams import StreamNameBuilder
from models.enums import Blockchains, DataType, Exchanges, StreamNames
import pandas as pd
import json
from utilities.common import generate_group_name
from utilities.logger import SetupLogger

_PATH_TO_REDIS_CONFIG = PATH_TO_HYPERLIQUID / "redis_config.json"
_redis_stream_manager = RedisStreamManager.from_config(_PATH_TO_REDIS_CONFIG)

_stream_name_builder = (
    StreamNameBuilder()
    .set("marketplace", Exchanges.HYPERLIQUID)
    .set("blockchain", Blockchains.COSMOS)
)
_REDIS_STREAMS = {
    "raw": {
        stream: _stream_name_builder.set("stream", stream)
        .set("data_type", DataType.RAW)
        .name
        for stream in StreamNames
    },
    "adapted": {
        stream: _stream_name_builder.set("stream", stream)
        .set("data_type", DataType.ADAPTED)
        .name
        for stream in StreamNames
    },
}


class HyperliquidAdapter(RawDataAdapter):
    def __init__(self):
        self.logger_config = SetupLogger(
            'hyperliquid_adapter', 'logs/hyperliquid/hyperliquid_adapter.log')
        self.logger = self.logger_config.create_logger()

    @_redis_stream_manager.publish_result(_REDIS_STREAMS["adapted"][StreamNames.PNL])
    async def get_oracle_prices(self, *args, **kwargs):
        """
        Get oracle prices for actively traded coins.

        :return: mapping between tickers and prices for all supported tokens

        Example:
        {"BTC/USD" : 39874.58, "ETH/USD" : 2645.55, "ARB/USD": 1.77}
        """
        try:
            stream_name = _REDIS_STREAMS["raw"][StreamNames.PRICES]
            self.logger.debug(
                "Reading raw data from redis at Hyperliquid_adapter.get_oracle_prices ")
            group_name = generate_group_name(stream_name)
            await _redis_stream_manager.create_redis_consumer_group(
                stream_name,
                group_name,
            )

            data = await _redis_stream_manager.xreadgroup(
                streams={stream_name: ">"},
                consumername="adapter",
                groupname=group_name,
                count=1,
                block=5,
            )

            if data:
                self.logger.info(
                    "Raw data received from redis at Hyperliquid_adapter.get_oracle_prices: %s ", data)
                # Extract prices from the data
                prices_data = data[0][1][0][1]

                oracle_prices = {f"{ticker.decode()}/USD": float(price.decode())
                                for ticker, price in prices_data.items()}
                self.logger.info(
                    "Publishing adapted data to redis: %s ", json.dumps(oracle_prices))
                return json.dumps(oracle_prices)
            else:
                self.logger.debug(
                    "No data received yet from redis at Hyperliquid_adapter.get_oracle_prices")
        except Exception as e:
            self.logger.error(
                f"An error occurred while fetching oracle prices: {e}")
            return None


    async def get_funding_rates(self, *args, **kwargs) -> dict[str, float]:
        pass

    @_redis_stream_manager.publish_result(_REDIS_STREAMS["adapted"][StreamNames.ORDER_BOOK])
    async def get_orderbook(self, ticker: str, *args, **kwargs) -> pd.DataFrame:
        pass

    async def get_liquidation_prices(self, *args, **kwargs) -> dict[str, float]:
        pass

    async def get_positions(self, account: str, *args, **kwargs) -> pd.DataFrame:
        pass

    async def get_trade_history(self, account: str, *args, **kwargs) -> pd.DataFrame:
        pass

    async def get_open_orders(self, account: str, *args, **kwargs) -> pd.DataFrame:
        pass

    async def get_order_history(self, account: str, *args, **kwargs) -> pd.DataFrame:
        pass

    async def pool(self, stream_name):
        self.logger.debug(
            "Pooling the data with get_oracle_prices currently with stream name %s ", stream_name)
        while True:
            try:
                group_name = generate_group_name(stream_name)
                await _redis_stream_manager.create_redis_consumer_group(
                    stream_name,
                    group_name,
                )

                data = await _redis_stream_manager.xreadgroup(
                    streams={stream_name: ">"},
                    consumername="adapter",
                    groupname=group_name,
                    count=1,
                    block=5,
                )

                yield data

            except Exception as e:
                self.logger.debug(
                    f"An error occurred while pool for data: {e}")
                continue
