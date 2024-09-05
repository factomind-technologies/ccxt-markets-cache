# ccxt-markets-cache

`ccxt-markets-cache` is a utility class for caching CCXT markets data to disk,
designed to improve performance for scripts using the CCXT library.
This cache reduces the time and resources needed to load markets data by storing it locally,
thus minimizing network traffic and CPU load when multiple scripts are running on the same machine.

## Why Use ccxt-markets-cache?

### Improved Performance for Repeated Data Fetching

When fetching OHLCV data or other market information using CCXT,
each instance requires loading the markets data by calling `load_markets()`.
This data is often large, containing various details such as tick size, quantity limits, and more.
Not only does fetching this data repeatedly cause high network traffic,
but it also imposes a significant load on your CPU to parse the JSON data into Python dictionaries.
`ccxt-markets-cache` solves this problem by caching the markets data to disk, which reduces both network and CPU usage.

### Handling Multiple Scripts and Race Conditions

If you have multiple scripts running concurrently on the same machine, each script needs to load the markets data.
Even with caching, concurrent scripts might attempt to write or read from the cache simultaneously,
leading to race conditions. `ccxt-markets-cache` handles this by managing access to the cache,
ensuring that all scripts can safely read from and write to the cached data without conflicts.

### Cache Expiration and Cleanup

The cache persists for 24 hours, and the cached file is stored at
`~/.cache/ccxt-markets/{YYYY-mm-dd}/{ccxt_exchange_id}.pkl`.
Users are responsible for clearing old cache files periodically.
However, there is a planned feature to automate the clearing of old caches to further simplify cache management.

## Installation

You can clone this repository and install it like:

```
git clone https://github.com/factomind-technologies/ccxt-markets-cache.git
cd ccxt-markets-cache

# pip install -e .  # For editable installs
pip install .
```

## Usage

### Synchronous Example

The following example demonstrates how to use ccxt-markets-cache with synchronous code:

```python
import asyncio
import ccxt
from ccxt_markets_cache import MarketsCache

def test_sync():
    exch = ccxt.binance()
    mc = MarketsCache()
    asyncio.run(mc.set_markets(exch))

    market = exch.market("BTC/USDT")
    print(market)
    assert market is not None
```

### Asynchronous Example

The following example demonstrates how to use ccxt-markets-cache with asynchronous code:

```python
import ccxt.async_support as ccxt
from ccxt_markets_cache import MarketsCache

async def test_async():
    exch = ccxt.binance()
    mc = MarketsCache()
    await mc.set_markets(exch)

    market = exch.market("BTC/USDT")
    print(market)
    assert market is not None
```

## Future Improvements

Automatic Cache Cleanup: There is a planned feature to automatically clear old cache files to keep
the cache directory clean and prevent unnecessary disk usage.

## Disclaimer

The cache directory is `~/.cache/ccxt-markets/{YYYY-mm-dd}/{ccxt_exchange_id}.pkl`.
The user is responsible for managing and clearing this directory to prevent excessive disk usage.
Make sure to check your cache directory periodically and remove outdated cache files.

## Contributing

Contributions are welcome! If you have ideas for new features or improvements, please feel free to submit a pull request or open an issue on the repository.

## License

This project is licensed under the MIT License.
Feel free to customize and modify the content as needed for your project!
