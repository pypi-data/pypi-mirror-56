Fetches **World Price** of a Certain Symbol Concurrently


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
