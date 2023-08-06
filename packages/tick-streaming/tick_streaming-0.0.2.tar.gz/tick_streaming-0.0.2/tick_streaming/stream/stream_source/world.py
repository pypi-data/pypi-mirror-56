import asyncio

import random

from tick_streaming.stream import Tick
from tick_streaming.stream.stream_source.base import BaseStreamSource
from world_price import WorldPrice
from world_price.source import (
    BinancePriceSource,
    HuoBiPriceSource,
    OkExPriceSource
)


class World(BaseStreamSource):

    def __init__(self, logger, symbol, specific_conf, **kwargs):
        super().__init__(logger, symbol, specific_conf, **kwargs)

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

            price_source = [
                BinancePriceSource,
                HuoBiPriceSource,
                OkExPriceSource
            ]

            self.logger.info("stream source ({}) fetching world price from {}".format(
                self.name,
                [s.__name__ for s in price_source]
            ))
            world_price = WorldPrice(price_source, price_diff_tolerance=0.05)
            p = await world_price.get_price(self.symbol)

            if p:
                amount = self.generate_amount()
                tick = Tick(p, amount, self.symbol, random.choice([True, False]))
                self.logger.info('stream source ({}) crawled volume making tick: {}'.format(
                    self.name,
                    tick
                ))
                await self.on_tick(tick)
            else:
                self.logger.warning("stream source ({}) did not crawl a valid volume making price.")
        except Exception as e:
            self.logger.error("error crawling tick: {}.".format(e))
