import os
from api.hyperliquid.hyperliquid import HyperLiquid
from adapters.hyperliquid.hyperliquid_adapter import HyperliquidAdapter
import logging
import asyncio

os.makedirs('logs', exist_ok=True)

logger = logging.getLogger('hyperliquid_logger')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('logs/hyperliquid.log')

handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


async def main():
    try:
        hyperliquid = HyperLiquid(logger)
        response = await hyperliquid.get_all_mids()
        if response:
            hyperliquid_adapter = HyperliquidAdapter()
            processed_prices = await hyperliquid_adapter.get_oracle_prices()
            logger.debug(
                "Response from oracle processed_prices: %s", processed_prices)
        else:
            logger.error("Failed to retrieve all mids")
            print("Failed to retrieve all mids")
    except Exception as e:
        logger.exception("An error occurred in the main function: %s", e)

if __name__ == "__main__":
    asyncio.run(main())
