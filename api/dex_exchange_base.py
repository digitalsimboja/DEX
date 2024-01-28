"""DEX Exchange Base"""

import logging
from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urljoin

from requests import Session


class DEXExchangeBase(ABC):
    """
    Base DEX Exchange Instance

    **This is the entrypoint for all data from third parties.
    Do not alter the payloads received from third parties.
    Wrap all get-data methods with a redis stream manager to
    publish results for later adaptation. Make sure you are
    pushing correct data to correct stream.**

    **Make sure you have all the endpoint coded when you inherit
    this class**

    When we need to execute specifically against DEX Marketplaces.
    Utilize this object to standardize the required properties and
    methods to interact with said counterparties.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_qps: Optional[int] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Constructor for the DEXExchange api

        :param api_key: confidential api-key for generating a session
        :param api_qps: queries-per-second parameter for spacing api requests
        :param logger: generates a new logger for this module if null
        :return: new instance
        """
        self._api_key = api_key
        self._api_qps = api_qps
        self._logger = logger
        self._session = None

    @property
    def api_key(self) -> str | None:
        return self._api_key

    @property
    def api_qps(self) -> int | None:
        return self._api_qps

    @property
    def logger(self) -> logging.Logger | None:
        return self._logger

    @property
    @abstractmethod
    def base_rest_url(self) -> str:
        """Return the base REST url from which we can join endpoints"""

    @property
    @abstractmethod
    def base_websocket_url(self) -> str:
        """Return the base websocket url from which we can join endpoints"""

    @property
    @abstractmethod
    def rest_endpoint_urls(self) -> dict[str, str]:
        """
        Return the dictionary of available endpoint urls for a rest api

        Assign a unique key to reference each endpoint.
        Use the following example to illustrate how this
        mapping is expected to be structured.

        E.g.
        {
            'token': "tokens/%s",
            'token_listings': "tokens/%s/listings",
            'token_offer_received': "tokens/%s/offers_received",
            'token_activities': "tokens/%s/activities",
        }

        It is encouraged to pass endpoints as formatted strings
        so later get_endpoint_url can embed characters into the
        string itself. Be sure to reference the key for the endpoint
        in later get requests to the specific endpoint itself.
        """

    @property
    @abstractmethod
    def session_headers(self) -> dict[str, str]:
        """Get the headers we need for a https session"""

    @property
    def session(self) -> Session:
        """
        Return the requests.Session object instance

        Lazily initialize the session object. If the
        session does not already exist, we can easily
        create the session here and assign to the
        attributes for the session.

        :return: Session object
        """
        if self._session:
            return self._session
        self._session = Session()
        self._session.headers.update(self.session_headers)
        return self._session

    def get_rest_endpoint_url(
        self,
        endpoint_key: str,
        **endpoint_kwargs,
    ) -> str:
        """
        Build the url for an REST-based API's endpoint

        :param endpoint_key: endpoint key to identify which rest-based api endpoint we wish to use
        :param endpoint_kwargs: any kwargs that need to be added inside the endpoint's formatted string
        :return: url combining the endpoint with the endpoint

        Example.
        >>> self.base_rest_url = "www.xyz.com/"
        >>> self.rest_endpoint_urls = {
        >>>     "get_collection": "contracts/{contract_address}/detail"
        >>> }
        >>> self.get_endpoint_url(
        >>>     endpoint_key="get_collection",
        >>>     contract_address="0x12345678910",
        >>> )
        >>> "www.xyz.com/contracts/0x12345678910/detail"
        """
        populated_endpoint = self.rest_endpoint_urls[endpoint_key].format(
            **endpoint_kwargs
        )
        return urljoin(
            base=self.base_rest_url,
            url=populated_endpoint,
        )
