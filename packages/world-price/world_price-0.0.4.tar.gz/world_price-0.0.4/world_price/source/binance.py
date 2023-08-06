import logging

from world_price.http_utils import get
from world_price.source.base_price_source import BasePriceSource
from world_price.utils import symbol_format_conv, SymbolFormatEnum

logger = logging.getLogger("WORLD_PRICE")


class BinancePriceSource(BasePriceSource):

    @staticmethod
    async def get_binance_price(symbol, limit=5):
        logger.debug("Fetching World Price From Binance...")
        symbol_lower = symbol_format_conv(
            symbol,
            from_format=SymbolFormatEnum.UPPER_UNDERSCORE,
            to_format=SymbolFormatEnum.LOWER
        )
        symbol_upper = symbol_lower.upper()
        url = "https://api.binance.com/api/v1/trades"
        params = {
            "symbol": symbol_upper,
            "limit": limit,
        }
        resp = await get(url, params=params)
        logger.debug("Fetched World Price From Binance...")
        return float(resp[-1]["price"])

    async def get_price(self, symbol):
        return await self.get_binance_price(symbol)
