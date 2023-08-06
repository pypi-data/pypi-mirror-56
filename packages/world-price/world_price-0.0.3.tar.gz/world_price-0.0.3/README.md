<p align="center">
  <a href="http://bitsoda.com">
    <img width="60" src="https://bitsoda-static.oss-cn-shanghai.aliyuncs.com/img/Bitsoda-Logo200.jpg">
  </a>
</p>

## Fetches **World Price** of a Certain Symbol Concurrently

[![Downloads](https://pepy.tech/badge/world-price)](https://pepy.tech/project/world-price)


### Module Installation

```bash
$ pip install world-price
```

### How to use

```python
from world_price import WorldPrice
from world_price.source import BinancePriceSource, HuoBiPriceSource, MxcPriceSource


SYMBOL = "BTC_USDT"


async def main():

    price_source = [BinancePriceSource, HuoBiPriceSource, MxcPriceSource]

    wp = WorldPrice(price_source, price_diff_tolerance=3/5)

    p = await wp.get_price(SYMBOL)

    print(f"world price of {SYMBOL}: {p}")
```
