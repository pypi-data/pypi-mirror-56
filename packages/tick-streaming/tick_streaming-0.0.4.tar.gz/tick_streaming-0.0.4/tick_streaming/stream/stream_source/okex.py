import asyncio
import json
import zlib

import websockets


from tick_streaming.stream import Tick
from tick_streaming.stream.stream_source.base import BaseStreamSource
from tick_streaming.utils import symbol_format_conv, SymbolFormatEnum


class OkEx(BaseStreamSource):

    def __init__(self, logger, symbol, specific_conf, **kwargs):
        super().__init__(logger, symbol, specific_conf, **kwargs)

        self.reconnecting = False
        self.url = "wss://real.okex.com:8443/ws/v3"

        self.symbol_str = symbol_format_conv(self.symbol, SymbolFormatEnum.UPPER_UNDERSCORE, SymbolFormatEnum.UPPER_HYPHEN)

    async def start(self):
        self.logger.info("starting stream source ({})...".format(self.name))

        try:
            await self.connect_ws()
        except Exception as e:
            self.logger.error("error in stream source ({}): {}".format(self.name, e))
            await self.on_err()
        else:
            await self.start_streaming()

    async def start_streaming(self):

        tick_subscribe_msg = {
            "op": "subscribe",
            "args": ["spot/trade:{}".format(self.symbol_str)]
        }

        try:

            await self.ws_conn.send(json.dumps(tick_subscribe_msg))

            async for msg in self.ws_conn:
                await self.handle_ws_resp(msg)

        except Exception as e:
            self.logger.error("error subscribing tick: {}.".format(e))
            await self.on_err()
        finally:
            await self.ws_conn.close()

    async def connect_ws(self):

        try:
            self.logger.info("creating websocket connection, url: {}.".format(self.url))

            self.ws_conn = await asyncio.wait_for(websockets.connect(self.url), timeout=10)

        except asyncio.TimeoutError as e:

            self.logger.error("timeout creating websocket connection")
            raise e

        except Exception as e:
            self.logger.error("error while creating websocket connection: {}.".format(e))
            raise e
        else:
            self.logger.info("created websocket connection, url: {}.".format(self.url))
            self.reconnecting = False

    async def handle_ws_resp(self, msg):
        try:
            decompress = zlib.decompressobj(
                -zlib.MAX_WBITS
            )
            inflated = decompress.decompress(msg)
            inflated += decompress.flush()

            if inflated.decode() == "pong":
                self.logger.debug("server ponged...")
                return

            json_message = json.loads(inflated)
        except Exception as e:
            self.logger.error("on_data error: {} | raw_message: {}".format(e, msg))
        else:
            self.logger.debug("got ws response: {}.".format(json_message))

            if json_message.get("table") == "spot/trade":

                await self.process_tick_event(json_message.get("data"))

    async def process_tick_event(self, data):
        ticks = data
        if ticks:
            self.logger.info("{} ticks in this event.".format(len(ticks)))
            for tick in ticks:
                await self.on_tick(Tick(
                    float(tick["price"]),
                    self.modify_amount(float(tick["size"])),
                    self.symbol,
                    tick["side"] == "buy"
                ))
        else:
            self.logger.debug("no ticks in this event.")
