from dataclasses import dataclass, field
from typing import List

import numpy as np
import pandas as pd

from ..market import MarketAsset


@dataclass
class OptimizationAsset(MarketAsset):
    quantity: float = 0.0  # evitar el error

    expected_return: float = 0.0

    # Campos derivados que no se pasan al constructor
    returns: pd.Series = field(init=False)
    log_returns: pd.Series = field(init=False)

    mean_return: float = field(init=False)
    volatility: float = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.returns = self.prices.pct_change().dropna()
        self.log_returns = self.prices.pct_change().apply(lambda x: np.log(1 + x))
        self.mean_return = self.log_returns.mean()

        if self.expected_return < 0.001:
            self.expected_return = self.mean_return

        self.volatility = self.log_returns.std()

    @classmethod
    def to_dataframe(cls, assets: List["OptimizationAsset"]) -> pd.DataFrame:
        """Convert a list of OptimizationAsset objects to a pandas DataFrame."""
        if not assets:
            return pd.DataFrame()

        data = []
        for asset in assets:
            data.append(
                {
                    "ticker": asset.ticker,
                    "currency": asset.currency,
                    "quantity": asset.quantity,
                    "mean_return": asset.mean_return,
                    "expected_return": asset.expected_return,
                    "volatility": asset.volatility,
                    "returns_length": len(asset.returns),
                }
            )

        return pd.DataFrame(data)

    def __repr__(self):
        return (
            f"OptimizationAsset(ticker={self.ticker}, sector={self.sector}, currency={self.currency}, "
            f"quantity={self.quantity}, prices_length={len(self.prices)}, info_keys={list(self.info.keys())})"
        )
