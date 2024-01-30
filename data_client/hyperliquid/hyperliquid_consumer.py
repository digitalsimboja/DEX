import os
from typing import Dict
import json
import pandas as pd
from data_client.data_client import DataConsumer
from models.enums import Blockchains, Exchanges, StreamNames
from utilities.common import generate_group_name
from utilities.logger import SetupLogger


class HyperliquidConsumer(DataConsumer):
    def __init__(self, redis_url: str, exchange: Exchanges, blockchain: Blockchains):
        super().__init__(redis_url, exchange, blockchain)
        self.logger_config = SetupLogger(
            'hyperliquid_data_consumer', 'logs/hyperliquid_data_consumer.log')
        self.logger = self.logger_config.create_logger()

    async def get_oracle_prices(self, *args, **kwargs) -> dict[str, float]:
        """
        Get funding rates

        :return: mapping between tickers and funding rates for all supported tokens (annualized)

        Example:
        {"BTC/USD" : 0.20, "ETH/USD" : -0.05, "ARB/USD": 0.10}
        """

        try:
            stream_name = self.get_stream_name(StreamNames.PNL)
            group_name = generate_group_name(stream_name)
            self.logger.debug(
                'Consuming oracle prices from stream %s with group_name %s ', stream_name, group_name)
            await self.redis.create_redis_consumer_group(
                stream_name,
                group_name,
            )

            data = await self.redis.xreadgroup(
                streams={stream_name: ">"},
                consumername="consumer",
                groupname=group_name,
                count=1,
                block=5,
            )

            oracle_prices = data[0][1][0][1]
            self.logger.debug(
                "Data consumed by get_oracle_prices %s ", oracle_prices)
            return json.dumps(oracle_prices)

        except Exception as e:
            self.logger.exception(
                "Error occurred consuming oracle prices : %s", e)

    async def get_funding_rates(self, *args, **kwargs) -> dict[str, float]:
        pass

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
