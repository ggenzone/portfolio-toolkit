from typing import Optional
import pandas as pd
from .market_asset import MarketAsset

class OptimizationAsset(MarketAsset):
    def __init__(
        self,
        ticker: str,
        prices: pd.Series,
        info: dict,
        quantity: float,
        currency: Optional[str] = None,
    ):
        """
        Represents an optimization asset, extending MarketAsset with quantity.

        Args:
            ticker (str): The ticker symbol of the asset.
            prices (pd.Series): Historical price data for the asset.
            info (dict): Additional information about the asset (e.g., from a data provider).
            quantity (float): The quantity of the asset for analysis.
            currency (Optional[str]): The currency for the asset. If None, it is derived from the info.
        """
        super().__init__(ticker, prices, info, currency)
        self.quantity = quantity

    def __repr__(self):
        return (
            f"OptimizationAsset(ticker={self.ticker}, sector={self.sector}, currency={self.currency}, "
            f"quantity={self.quantity}, prices_length={len(self.prices)}, info_keys={list(self.info.keys())})"
        )