from enum import Enum


class Exchanges(Enum):
    HYPERLIQUID = "hyperliquid"
    VERTEX = "vertex"


class StreamNames(Enum):
    TRADES = "trades"
    PNL = "pnl"
    PRICES = "prices"
    ORDER_BOOK = "orderbook"


class Blockchains(Enum):
    SOLANA = "solana"
    ETHEREUM = "ethereum"
    COSMOS = "cosmos"


class DataType(Enum):
    ADAPTED = "adapted"
    RAW = "raw"
