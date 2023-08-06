import asyncio
import random

from tick_streaming.stream import Tick
from tick_streaming.stream.stream_source.base import BaseStreamSource


class Internal(BaseStreamSource):

    def __init__(self, logger, symbol, specific_conf, **kwargs):
        super().__init__(logger, symbol, specific_conf, **kwargs)

        self.trade_engine = kwargs.pop("trade_engine")

    async def start(self):
        self.logger.info("starting stream source ({})...".format(self.name))
        while True:
            try:
                await self.crawl_tick()
            except Exception as e:
                self.logger.error("error in stream source ({}): {}".format(self.name, e))
            finally:
                await asyncio.sleep(random.random() * self.specific_conf["volume_making_frequency"])

    async def crawl_tick(self):
        try:
            internal_volume_making_price = await self.trade_engine.get_internal_volume_making_price(self.symbol)
            if internal_volume_making_price:
                amount = self.generate_amount()
                tick = Tick(internal_volume_making_price, amount, self.symbol, random.choice([True, False]))
                self.logger.info('stream source ({}) crawled volume making tick: {}'.format(
                    self.name,
                    tick
                ))
                await self.on_tick(tick)
            else:
                self.logger.warning("internal stream source did not crawl a valid volume making price.")
        except Exception as e:
            self.logger.error("error crawling tick: {}.".format(e))
