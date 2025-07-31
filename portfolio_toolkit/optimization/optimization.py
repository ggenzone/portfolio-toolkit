from dataclasses import dataclass
from typing import List, Optional

import pandas as pd

from portfolio_toolkit.asset.optimization_asset import OptimizationAsset
from portfolio_toolkit.data_provider.data_provider import DataProvider
from portfolio_toolkit.math.get_matrix_returns import get_matrix_returns
from portfolio_toolkit.math.get_var import get_covariance_matrix


@dataclass
class Optimization:
    """
    Class to represent and manage an asset optimization.
    """

    name: str
    currency: str
    assets: List[OptimizationAsset]
    data_provider: DataProvider
    returns: Optional[pd.DataFrame] = None
    covariance_matrix: Optional[pd.DataFrame] = None
    weights: Optional[pd.Series] = None

    def __post_init__(self):
        if not self.assets:
            raise ValueError("Optimization must have at least one asset.")

        self.weights = pd.Series([asset.quantity for asset in self.assets])
        self.returns = get_matrix_returns(self.assets)
        self.covariance_matrix = get_covariance_matrix(self.assets)

    def __repr__(self):
        return f"Optimization(name={self.name}, currency={self.currency}, assets_count={len(self.assets)})"
