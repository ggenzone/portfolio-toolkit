from dataclasses import dataclass
from typing import List

from portfolio_toolkit.asset import MarketAsset
from portfolio_toolkit.data_provider.data_provider import DataProvider


@dataclass
class Watchlist:
    """
    Class to represent and manage an asset watchlist.
    """

    name: str
    currency: str
    assets: List[MarketAsset]
    data_provider: DataProvider

    @classmethod
    def from_dict(cls, data: dict, data_provider: DataProvider) -> "Watchlist":
        from .watchlist_from_dict import create_watchlist

        """
        Alternate constructor that builds Watchlist from a dictionary.
        """
        return create_watchlist(data, data_provider)

    def __repr__(self):
        return f"Watchlist(name={self.name}, currency={self.currency}, assets_count={len(self.assets)})"
