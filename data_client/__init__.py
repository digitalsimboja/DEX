import json
from abc import ABC

from caching.stream_manager import RedisStreamManager


class DexDataClient(ABC):
    _REDIS_URL = ""

    """
    Read internally adapted data via the redis stream manager from an exposed REDIS cache of DEX data 
    """

    def __init__(self):
        """"""

    @abstractmethod
    async def fetch_exchange_info(self, *args, **kwargs) -> Response:
        """
        Fetch exchange metadata

        :return: Response with exchange metadata
        """

    @abstractmethod
    async def fetch_funding_rate(self, *args, **kwargs) -> Response:
        """
        Fetch Funding Rate

        :return: Response with funding rate
        """

    @abstractmethod
    async def fetch_orderbook(self, *args, **kwargs) -> Response:
        """
        Fetch l2orderbook data

        :return: Response with orderbook
        """

    @abstractmethod
    async def fetch_liquidation_rates(self, *args, **kwargs) -> Response:
        """
        Fetch Liquidation Rates

        :return: Response with liquidation rates
        """

    @abstractmethod
    async def fetch_positions(self, *args, **kwargs) -> Response:
        """
        get traders' positions

        :return: Response with other traders' positions
        """

    @abstractmethod
    async def fetch_wallet_activities(self, *args, **kwargs) -> Response:
        """
        Fetch Wallet Activities

        :return: Response with wallet activities
        """

    """Dex Private API"""

    @abstractmethod
    def limit_order(self, *args, **kwargs) -> Response:
        """
        Create an individual limit order

        :return: Response with limit order result
        """

    @abstractmethod
    def cancel_order(self, *args, **kwargs) -> Response:
        """
        Cancel an individual order

        :return: Response with cancel order result
        """

    @abstractmethod
    def market_order(self, *args, **kwargs) -> Response:
        """
        Market order for individual dex

        :return: Response of market order result
        """

    @abstractmethod
    def order_status(self, *args, **kwargs) -> Response:
        """
        get order status

        :return: Response of order status result
        """
