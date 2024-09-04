import asyncio

import ccxt

from ccxt_markets_cache import MarketsCache


def test_sync():
    # You need to run twice to ensure that the data is read from the disk,
    # without fetching it from the exchange.
    for _ in range(2):
        exch = ccxt.binance()
        mc = MarketsCache()
        asyncio.run(mc.set_markets(exch))

        market = exch.market("BTC/USDT")
        print(market)
        assert market is not None
