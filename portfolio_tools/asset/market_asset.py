from typing import Optional

import pandas as pd


class MarketAsset:
    def __init__(
        self, ticker: str, prices: pd.Series, info: dict, currency: Optional[str] = None
    ):
        """
        Represents a market asset with associated data.

        Args:
            ticker (str): The ticker symbol of the asset.
            prices (pd.Series): Historical price data for the asset.
            info (dict): Additional information about the asset (e.g., from a data provider).
            currency (Optional[str]): The currency for the asset. If None, it is derived from the info.
        """
        self.ticker = ticker
        self.sector = info.get("sector", "Unknown")
        self.country = info.get("country", "Unknown")
        self.prices = prices
        self.info = info
        self.currency = currency or info.get("currency", "Unknown")

    def __repr__(self):
        return (
            f"MarketAsset(ticker={self.ticker}, sector={self.sector}, currency={self.currency}, "
            f"prices_length={len(self.prices)}, info_keys={list(self.info.keys())})"
        )
