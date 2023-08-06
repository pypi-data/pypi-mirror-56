from datetime import datetime
from collections import namedtuple

from logging import getLogger

logger = getLogger("RetryTicksContainer")
RetryTick = namedtuple("RetryTick", ["schedule_time", "tick_object"])


class RetryContainer(object):

    def __init__(self):
        self._symbol = None

        self.pending_retry_ticks = []

    def set_symbol(self, symbol):
        self._symbol = symbol

    async def get_retry_ticks(self, configs):

        _pending_retry_ticks = self.pending_retry_ticks

        self.pending_retry_ticks = []

        _retry_ticks = []

        for _retry_tick in _pending_retry_ticks:
            if (datetime.now() - _retry_tick.schedule_time).seconds > configs["tick_expire_time"]:
                logger.debug("expired RetryTick: {}, drop it".format(_retry_tick))
                _pending_retry_ticks.remove(_retry_tick)
            else:
                _retry_ticks.append(_retry_tick.tick_object)

        logger.info("{} RetryTicks this round".format(len(_retry_ticks)))

        return _retry_ticks

    async def retry_later(self, tick):
        if list(filter(lambda t: t.tick_object.price == tick.price, self.pending_retry_ticks)):
            logger.debug("duplicate RetryTick: {}, drop it".format(tick))
        else:
            self.pending_retry_ticks.append(
                RetryTick(datetime.now(), tick)
            )


retry_container = RetryContainer()
