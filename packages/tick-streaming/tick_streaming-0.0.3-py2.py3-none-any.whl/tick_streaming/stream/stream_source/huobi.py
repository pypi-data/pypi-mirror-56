import asyncio
import gzip
import json

import websockets


from tick_streaming.stream import Tick
from tick_streaming.stream.stream_source.base import BaseStreamSource
from tick_streaming.utils import symbol_format_conv, SymbolFormatEnum


class Huobi(BaseStreamSource):

    def __init__(self, logger, symbol, specific_conf, **kwargs):
        super().__init__(logger, symbol, specific_conf, **kwargs)

        self.reconnecting = False
        self.url = "wss://api.huobi.pro/ws"

        _symbol_str = symbol_format_conv(self.symbol, SymbolFormatEnum.UPPER_UNDERSCORE, SymbolFormatEnum.LOWER)

        self.channel = "market.{}.trade.detail".format(_symbol_str)
        self.error_times = 0

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

        depth_subscribe_msg = {
            "sub": self.channel
        }

        try:

            await self.ws_conn.send(json.dumps(depth_subscribe_msg))

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

    async def on_err(self):

        self.error_times += 1

        if self.ws_conn is not None and not self.ws_conn.closed:
            await self.ws_conn.close()
        reconnect_wait_time = min([2 * self.error_times, 60])
        self.logger.info("websocket reconnect frequency limit: reconnect in {} seconds.".format(reconnect_wait_time))
        await asyncio.sleep(reconnect_wait_time)
        await self.start()

    async def handle_ws_resp(self, msg):
        try:
            str_message = gzip.decompress(msg).decode("utf-8")
            json_message = json.loads(str_message)
        except Exception as e:
            self.logger.error("on_data error: {} | raw_message: {}".format(e, msg))
        else:
            self.logger.debug("got ws response: {}.".format(json_message))

            _ping_nonce = json_message.get("ping", None)

            if _ping_nonce is not None:
                await self.ws_conn.send(json.dumps({
                    "pong": _ping_nonce
                }))
                self.logger.debug("got ping msg with nonce {}, then ponged...".format(_ping_nonce))
                return

            if json_message.get("ch") == self.channel:
                await self.process_tick_event(json_message.get("tick"))

    async def process_tick_event(self, data):
        ticks = data.get("data", [])
        if ticks:
            self.logger.info("{} ticks in this event.".format(len(ticks)))
            for tick in ticks:
                await self.on_tick(Tick(
                    float(tick["price"]),
                    self.modify_amount(float(tick["amount"])),
                    self.symbol,
                    tick["direction"] == "buy"
                ))
        else:
            self.logger.debug("no ticks in this event.")
