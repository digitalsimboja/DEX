from __future__ import annotations

from enum import Enum
from typing import Literal, Type

from models.enums import Blockchains, DataType, Exchanges, StreamNames


class StreamNameBuilder:
    """
    Builder pattern to
    """

    def __init__(self):
        self._marketplace = None
        self._stream = None
        self._blockchain = None
        self._data_type = None

    @property
    def marketplace(self) -> str:
        return self._marketplace

    @property
    def stream(self) -> str:
        return self._stream

    @property
    def blockchain(self) -> str:
        return self._blockchain

    @property
    def data_type(self) -> str:
        return self._data_type

    @marketplace.setter
    def marketplace(self, exchange: Exchanges):
        self._marketplace = exchange.value

    @stream.setter
    def stream(self, name: StreamNames):
        self._stream = name.value

    @blockchain.setter
    def blockchain(self, blockchain: Blockchains):
        self._blockchain = blockchain.value

    @data_type.setter
    def data_type(self, dt: DataType):
        self._data_type = dt.value

    @property
    def name(self) -> str:
        for att in [self.marketplace, self.stream, self.blockchain, self.data_type]:
            if att is None:
                raise ValueError("Missing value necessary to build a stream name")
        return f"{self.data_type}-{self.marketplace}-{self.blockchain}-{self.stream}"

    def set(
        self,
        key: Literal["blockchain", "marketplace", "stream", "data_type"],
        value: Type[Enum],
    ) -> StreamNameBuilder:
        """Pipe a setter command for easier use-cases of the builder"""
        setattr(self, key, value)
        return self
