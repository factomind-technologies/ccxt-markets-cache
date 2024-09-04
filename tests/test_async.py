import ccxt.async_support as ccxt
import pytest

from ccxt_markets_cache import MarketsCache

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_async():
    # You need to run twice to ensure that the data is read from the disk,
    # without fetching it from the exchange.
    for _ in range(2):
        exch = ccxt.binance()
        mc = MarketsCache()
        await mc.set_markets(exch)

        market = exch.market("BTC/USDT")
        print(market)
        assert market is not None
