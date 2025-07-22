from typing import List

from portfolio_tools.asset.market_asset import MarketAsset
from portfolio_tools.data_provider.data_provider import DataProvider


class Watchlist:
    """
    Class to represent and manage an asset watchlist.
    """

    def __init__(
        self,
        name: str,
        currency: str,
        assets: List[MarketAsset],
        data_provider: DataProvider,
    ):
        """
        Initializes the Watchlist class and optionally loads data from a JSON file.

        Args:
            json_filepath (str, optional): Path to the JSON file to load data from.
            data_provider (DataProvider, optional): Data provider to obtain historical prices.

        Returns:
            None
        """
        self.name = name
        self.currency = currency
        self.assets = assets
        self.data_provider = data_provider  # Data provider

    def __repr__(self):
        return f"Watchlist(name={self.name}, currency={self.currency}, assets_count={len(self.assets)})"
