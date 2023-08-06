import asyncio
import logging

from world_price.http_utils import get
from world_price.source.base_price_source import BasePriceSource
from world_price.utils import symbol_format_conv, SymbolFormatEnum

logger = logging.getLogger("WORLD_PRICE")


class HuoBiPriceSource(BasePriceSource):

    @staticmethod
    async def get_huobi_price(symbol):
        logger.debug("Fetching World Price From HuoBi...")
        symbol_lower = symbol_format_conv(
            symbol,
            from_format=SymbolFormatEnum.UPPER_UNDERSCORE,
            to_format=SymbolFormatEnum.LOWER
        )
        url = 'https://api.huobi.pro/market/trade?symbol={}'.format(symbol_lower)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0"
        }
        resp = await get(url, headers=headers)

        if resp['status'] == "error":
            # fallback option
            revert_symbol = symbol_format_conv(
                symbol_lower,
                from_format=SymbolFormatEnum.LOWER,
                to_format=SymbolFormatEnum.LOWER_UNDERSCORE
            )
            url1 = 'https://api.huobi.pro/market/trade?symbol=%s' % (revert_symbol.split("_")[0] + "usdt")
            url2 = 'https://api.huobi.pro/market/trade?symbol=%s' % (revert_symbol.split("_")[1] + "usdt")
            _tasks = [
                asyncio.ensure_future(get(url1, headers=headers, timeout=5)),
                asyncio.ensure_future(get(url2, headers=headers, timeout=5)),
            ]
            # todo `done` set is not ordered
            done, _pending = await asyncio.wait(_tasks)
            task1, task2 = done
            resp1 = task1.result()
            resp2 = task2.result()
            p1 = resp1['tick']['data'][0]['price']
            p2 = resp2['tick']['data'][0]['price']
            p = '%.8f' % (p1 / p2)
        else:
            p = resp['tick']['data'][0]['price']
        logger.debug("Fetched World Price From HuoBi...")
        return p

    async def get_price(self, symbol):
        return await self.get_huobi_price(symbol)
