import asyncio
from adapters.hyperliquid.hyperliquid_adapter import HyperliquidAdapter
from utilities.logger import SetupLogger

async def main():
    # Configure logger
    logger_config = SetupLogger("hyperliquid_job_logger", "hyperliquid_job.log" )
    logger = logger_config.create_logger()
    hyperliquidAdapter = HyperliquidAdapter()

    while True:
        try:
            tasks = [
                hyperliquidAdapter.get_oracle_prices(),
                # hyperliquidAdapter.get_funding_rates(),
                # hyperliquidAdapter.get_orderbook("BTC/USD"),
            ]
            # Gather tasks, but do not await here to keep the loop running
            asyncio.gather(*tasks)
            
            # Add a sleep to control the frequency of task executions
            await asyncio.sleep(10)  # Adjust as needed
        except Exception as e:
            logger.debug(f"An error occurred: {e}")
            continue

if __name__ == "__main__":
    asyncio.run(main())
