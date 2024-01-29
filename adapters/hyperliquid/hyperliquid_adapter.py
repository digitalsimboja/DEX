from adapters.dex_adapter_base import RawDataAdapter
from api.hyperliquid.constants import PATH_TO_HYPERLIQUID
from caching.stream_manager import RedisStreamManager
from caching.streams import StreamNameBuilder
from models.enums import Blockchains, DataType, Exchanges, StreamNames
import pandas as pd
import json
from typing import Dict

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
        pass

    @_redis_stream_manager.publish_result(_REDIS_STREAMS["adapted"][StreamNames.PNL])
    async def get_oracle_prices(self, *args, **kwargs):
        """
        Get oracle prices for actively traded coins.

        :return: mapping between tickers and prices for all supported tokens

        ** Ignoring the timestamp data until required by data consumer**

        Example:
        {"BTC/USD" : 39874.58, "ETH/USD" : 2645.55, "ARB/USD": 1.77}
        """
        group_name = f"{_REDIS_STREAMS['raw'][StreamNames.PRICES]}_consumer"
        await _redis_stream_manager.create_redis_consumer_group(
            _REDIS_STREAMS["raw"][StreamNames.PRICES],
            group_name,
        )

        data = await _redis_stream_manager.xreadgroup(
            streams={_REDIS_STREAMS["raw"][StreamNames.PRICES]: ">"},
            consumername="adapter",
            groupname=group_name,
            count=1,
            block=5,
        )
        # Extract prices from the data
        prices_data = data[0][1][0][1]

        # Format data to include the USD ticker
        # Convert bytes-like object keys and values to strings and floats respectively
        oracle_prices = {f"{ticker.decode()}/USD": float(price.decode())
                         for ticker, price in prices_data.items()}

        return json.dumps(oracle_prices)

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
