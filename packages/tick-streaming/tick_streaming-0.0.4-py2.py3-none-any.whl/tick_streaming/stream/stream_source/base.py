import asyncio
import random


class BaseStreamSource(object):

    def __init__(self, logger, symbol, specific_conf, **kwargs):
        self.logger = logger
        self.symbol = symbol

        self.specific_conf = specific_conf

        self.ws_conn = None
        self.observer = None

        self.error_times = 0

        self.gen_amount_func = kwargs.get("gen_amount_func")

    @property
    def name(self):
        return self.__class__.__name__

    def start(self):
        pass

    def attach(self, observer):
        self.logger.info("will notify {} once I ({}) have a tick.".format(observer.__class__.__name__, self.name))
        self.observer = observer

    async def on_tick(self, tick):
        self.logger.info("{} pushing tick: {}".format(
            self.name,
            tick
        ))
        _cb = self.observer.push_ticks
        if asyncio.iscoroutinefunction(_cb):
            await _cb(tick)
        else:
            _cb(tick)

    def modify_amount(self, amount):
        _ratio = self.specific_conf.get("amount_adjust_ratio", 1)
        return amount * _ratio

    def generate_amount(self):

        if self.gen_amount_func:

            return self.gen_amount_func()

        return random.random()

    async def on_err(self):

        self.error_times += 1

        if self.ws_conn is not None and not self.ws_conn.closed:
            await self.ws_conn.close()
        reconnect_wait_time = min([2 * self.error_times, 60])
        self.logger.info("websocket reconnect frequency limit: reconnect in {} seconds.".format(reconnect_wait_time))
        await asyncio.sleep(reconnect_wait_time)
        await self.start()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
