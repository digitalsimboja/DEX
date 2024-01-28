from adapters.dex_adapter_base import RawDataAdapter
from api.hyperliquid.constants import PATH_TO_HYPERLIQUID
from caching.stream_manager import RedisStreamManager
from caching.streams import StreamNameBuilder
from models.enums import Blockchains, DataType, Exchanges, StreamNames

_PATH_TO_REDIS_CONFIG = PATH_TO_HYPERLIQUID / "redis_config.json"
_redis_stream_manager = RedisStreamManager.from_config(_PATH_TO_REDIS_CONFIG)

_stream_name_builder = (
    StreamNameBuilder()
    .set("marketplace", Exchanges.HYPERLIQUID)
    .set("blockchain", Blockchains.HYPERLIQUID)
)
_REDIS_STREAMS = {
    "raw": {
        stream: _stream_name_builder.set("stream", stream)
        .set("data_type", DataType.RAW)
        .name
        for stream in StreamNames
    },
    "adapted": {
        stream: _stream_name_builder.set("stream", stream)
        .set("data_type", DataType.ADAPTED)
        .name
        for stream in StreamNames
    },
}


class HyperliquidAdapter(RawDataAdapter):

    @_redis_stream_manager.publish_result(_REDIS_STREAMS["adapted"][StreamNames.PNL])
    async def example_method(self):
        await _redis_stream_manager.create_redis_consumer_group(
            _REDIS_STREAMS["raw"][StreamNames.PNL],
            "group_name",
        )

        data = await _redis_stream_manager.xreadgroup(
            streams={_REDIS_STREAMS["raw"][StreamNames.PNL]: ">"},
            consumername="adapter",
            groupname="group_name",
            count=1,
            block=5,
        )

        return data
