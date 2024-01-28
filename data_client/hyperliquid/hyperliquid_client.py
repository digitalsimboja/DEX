import os
from api.hyperliquid.hyperliquid import HyperLiquid
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

def main():
    logger.debug("Starting main function")
    try:
        hyperliquid = HyperLiquid(logger)
        response = asyncio.run(hyperliquid.get_all_mids())
        if response:
            data = response.json()
            logger.debug("Response from get_all_mids: %s", data)
            print("Response from get_all_mids:")
            print(data)
        else:
            logger.error("Failed to retrieve all mids")
            print("Failed to retrieve all mids")
    except Exception as e:
        logger.exception("An error occurred in the main function: %s", e)

if __name__ == "__main__":
    main()