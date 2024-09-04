import asyncio
import pickle
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ccxt.async_support as ccxt
import fasteners
from logzero import logger


class MarketsCache:
    def __init__(self):
        self.currencies: dict[str, Any] = {}
        self.markets: dict[str, Any] = {}
        self.options: dict[str, Any] = {}

    def _cache_filename(self, exid: str) -> Path:
        today: str = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        return Path(f"~/.cache/ccxt-markets/{today}/{exid}.pkl").expanduser()

    def _save_state(self, cachef: Path, state: dict[str, Any]):
        # Pickle the state
        with cachef.open("wb") as f:
            pickle.dump(state, f)

    def _load_state(self, cachef: Path) -> dict[str, Any]:
        with cachef.open("rb") as f:
            return pickle.load(f)

    async def _fetch_currencies(self, exch: ccxt.Exchange):
        cachef: Path = self._cache_filename(exch.id)
        cachef.parent.mkdir(parents=True, exist_ok=True)

        lockf = str(cachef) + ".lock"
        rw_lock = fasteners.InterProcessReaderWriterLock(lockf)  # for processes
        with rw_lock.write_lock():
            if cachef.exists():
                logger.debug("MarketsCache: Using %s for exchange %s", cachef, exch.id)
                return self._load_state(cachef)

            logger.debug("MarketsCache: Fetching markets for exchange %s", exch.id)
            if asyncio.iscoroutinefunction(exch.load_markets):
                await exch.load_markets()
            else:
                exch.load_markets()

            state = {
                "currencies": exch.currencies,
                "markets": exch.markets,
                "options": exch.options,
            }
            self._save_state(cachef, state)
            return state

    async def set_markets(self, exch: ccxt.Exchange):
        state = await self._fetch_currencies(exch)
        markets = state["markets"]
        currencies = state["currencies"]
        options = state["options"]
        exch.set_markets(markets, currencies)

        # For huobi...
        # For transfers to work.
        # huobi.fetch_currencies() side effect.
        keys = ["networkNamesByChainIds", "networkChainIdsByNames"]
        for key in keys:
            if key in options:
                exch.options[key] = options[key]
