import logging

from world_price.http_utils import get
from world_price.source.base_price_source import BasePriceSource

logger = logging.getLogger("WORLD_PRICE")


class MxcPriceSource(BasePriceSource):

    @staticmethod
    async def get_mxc_price(symbol):
        logger.debug("Fetching World Price From MXC...")
        symbol_upper_underscore = symbol
        root_url = 'https://www.mxc.ceo'
        url = root_url + '/open/api/v1/data/history'
        params = {
            "market": symbol_upper_underscore,
        }
        resp = await get(url, params=params)
        logger.debug("Fetched World Price From MXC...")
        return float(resp["data"][0]["tradePrice"])

    async def get_price(self, symbol):
        return await self.get_mxc_price(symbol)
