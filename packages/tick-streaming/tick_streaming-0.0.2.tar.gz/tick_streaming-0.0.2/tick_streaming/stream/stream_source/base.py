import asyncio
import random


class BaseStreamSource(object):

    def __init__(self, logger, symbol, specific_conf, **kwargs):
        self.logger = logger
        self.symbol = symbol

        self.specific_conf = specific_conf

        self.ws_conn = None
        self.observer = None

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

        _max = self.specific_conf["volume_making_max_amount"]
        _min = self.specific_conf["volume_making_min_amount"]

        return _min + (_max - _min) * random.random()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
