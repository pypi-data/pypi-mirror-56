import logging

from world_price.http_utils import get
from world_price.source.base_price_source import BasePriceSource
from world_price.utils import symbol_format_conv, SymbolFormatEnum

logger = logging.getLogger("WORLD_PRICE")


class OkExPriceSource(BasePriceSource):

    @staticmethod
    async def get_okex_price(symbol, limit=5):
        """
        https://www.okex.com/api/spot/v3/instruments/<instrument_id>/trades
        """
        logger.debug("Fetching World Price From OkEx...")
        upper_hyphen_symbol = symbol_format_conv(
            symbol,
            from_format=SymbolFormatEnum.UPPER_UNDERSCORE,
            to_format=SymbolFormatEnum.UPPER_HYPHEN
        )
        url = "https://www.okex.com/api/spot/v3/instruments/{}/trades".format(upper_hyphen_symbol)
        params = {
            "limit": limit,
        }
        resp = await get(url, params=params)
        logger.debug("Fetched World Price From OkEx...")
        return float(resp[0]["price"])

    async def get_price(self, symbol):
        return await self.get_okex_price(symbol)
