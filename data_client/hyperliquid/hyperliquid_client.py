import os
from typing import Dict
import json
import pandas as pd
from api.hyperliquid.hyperliquid import HyperLiquid
from adapters.hyperliquid.hyperliquid_adapter import HyperliquidAdapter
import logging
import asyncio
from data_client.data_client import DataConsumer
from models.enums import Blockchains, Exchanges, StreamNames

os.makedirs('logs', exist_ok=True)


logger = logging.getLogger('hyperliquid_logger')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('logs/hyperliquid.log')

handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


class HyperliquidClient(DataConsumer):
    def __init__(self, redis_url: str, exchange: Exchanges, blockchain: Blockchains):
        super().__init__(redis_url, exchange, blockchain)
        self.hyperliquid = HyperLiquid(logger)
        self.hyperliquid_adapter = HyperliquidAdapter()

    async def get_oracle_prices(self, *args, **kwargs) -> dict[str, float]:
        """
        Get funding rates

        :return: mapping between tickers and funding rates for all supported tokens (annualized)

        Example:
        {"BTC/USD" : 0.20, "ETH/USD" : -0.05, "ARB/USD": 0.10}
        """
        try:
            # Get the data from external API
            await self.hyperliquid.get_all_mids()
            # Adapt the data
            await self.hyperliquid_adapter.get_oracle_prices()
            # Read the adapted data
            # TODO: Use the get_stream_name base function
            stream_name = "adapted-hyperliquid-cosmos-pnl"
            group_name = f"{stream_name}_consumer"
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
            return json.dumps(oracle_prices)

        except Exception as e:
            logger.exception("Error occurred : %s", e)

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


async def main():
    client = HyperliquidClient(redis_url="redis://redis:6379/0",
                               exchange=Exchanges.HYPERLIQUID,
                               blockchain=Blockchains.COSMOS)
    data = await client.get_oracle_prices()
    logger.debug("Read adapated data from oracle %s", data)

if __name__ == '__main__':
    asyncio.run(main())
