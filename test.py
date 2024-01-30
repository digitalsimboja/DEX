import asyncio
from api.hyperliquid.hyperliquid import HyperLiquid
from data_client.hyperliquid.hyperliquid_consumer import HyperliquidConsumer
from models.enums import Blockchains, Exchanges


async def consume_data():
    try:
        client = HyperliquidConsumer(redis_url="redis://redis:6379/0",
                                     exchange=Exchanges.HYPERLIQUID,
                                     blockchain=Blockchains.COSMOS)
        data = await client.get_oracle_prices()
        print("Read adapted data from oracle %s", data)
    except Exception as e:
        print(f"An error occurred during data consumption: {e}")


async def main():
    try:
        hyperliquid = HyperLiquid()
        await hyperliquid.get_all_mids()
        await consume_data()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
