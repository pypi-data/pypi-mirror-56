import asyncio
import logging

from world_price.adapter import WorldPriceAdapter
from world_price.utils import validate_world_price

logger = logging.getLogger("WORLD_PRICE")


class WorldPrice(object):

    def __init__(self, source: list, price_diff_tolerance=5 / 100):
        self.source = list(set(source))
        self.price_diff_tolerance = price_diff_tolerance

    async def get_price(self, symbol):
        logger.debug("Fetching World Price...")
        tasks = []
        for _source in self.source:
            adapter = WorldPriceAdapter(_source)
            tasks.append(asyncio.ensure_future(adapter.get_price(symbol)))
        done, _pending = await asyncio.wait(tasks)
        world_prices = [task.result() for task in done if task.exception() is None]
        if world_prices:
            return validate_world_price(world_prices, self.price_diff_tolerance)
        msg = "All Price Source DOWN!"
        logger.error(msg)
        raise Exception(msg)
