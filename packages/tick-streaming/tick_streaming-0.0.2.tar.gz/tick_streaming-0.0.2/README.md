<p align="center">
  <a href="http://bitsoda.com">
    <img width="60" src="https://bitsoda-static.oss-cn-shanghai.aliyuncs.com/img/Bitsoda-Logo200.jpg">
  </a>
</p>

## A Event Driven Tick Streaming Framework

[![Downloads](https://pepy.tech/badge/crypto-currency-world-price)](https://pepy.tech/project/crypto-currency-world-price)


### Module Installation

```bash
$ pip install tick_streaming
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
