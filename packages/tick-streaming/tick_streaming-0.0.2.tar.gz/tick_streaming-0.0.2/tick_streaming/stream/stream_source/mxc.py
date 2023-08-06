import socketio

from tick_streaming.stream import Tick
from tick_streaming.stream.stream_source.base import BaseStreamSource

sio = socketio.AsyncClient()


cache = object()  # just a dummy object


async def process_tick(data):
    symbol = data.get("symbol")
    ticks = data.get("data", {}).get("deals")
    if ticks:
        for tick in ticks:
            await cache.on_tick(Tick(
                float(tick["p"]),
                cache.modify_amount(float(tick["q"])),
                symbol,
                tick["T"] == 1
            ))
    else:
        cache.logger.debug("no ticks in this event.")


class Mxc(BaseStreamSource):

    def __init__(self, logger, symbol, specific_conf, **kwargs):
        super().__init__(logger, symbol, specific_conf, **kwargs)

        self.url = "wss://www.mxc.com"
        global cache
        cache = self

    async def start(self):
        self.logger.info("starting stream source ({})...".format(self.name))
        await sio.connect(self.url, transports="websocket")
        await sio.wait()

    @staticmethod
    @sio.on("push.symbol")
    async def on_tick_event(data):
        await process_tick(data)

    @staticmethod
    @sio.event
    async def connect():
        cache.logger.info("sio connected")
        await sio.emit("sub.symbol", data={"symbol": cache.symbol})
        cache.logger.info("emitted...")

    @staticmethod
    @sio.on("disconnect")
    async def disconnect():
        cache.logger.info("sio disconnected")
