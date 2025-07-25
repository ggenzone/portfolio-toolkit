from dataclasses import dataclass
from typing import List

from portfolio_tools.asset.market_asset import MarketAsset
from portfolio_tools.data_provider.data_provider import DataProvider


@dataclass
class Watchlist:
    """
    Class to represent and manage an asset watchlist.
    """

    name: str
    currency: str
    assets: List[MarketAsset]
    data_provider: DataProvider

    def __repr__(self):
        return f"Watchlist(name={self.name}, currency={self.currency}, assets_count={len(self.assets)})"
