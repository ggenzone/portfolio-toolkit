from dataclasses import dataclass
from typing import List, Optional

import pandas as pd

from portfolio_toolkit.asset import OptimizationAsset
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
    period: str = "1y"
    returns: Optional[pd.DataFrame] = None
    covariance_matrix: Optional[pd.DataFrame] = None
    means: Optional[pd.Series] = None
    weights: Optional[pd.Series] = None
    expected_returns: Optional[pd.Series] = None

    def __post_init__(self):
        if not self.assets:
            raise ValueError("Optimization must have at least one asset.")

        self.weights = pd.Series(
            [asset.quantity for asset in self.assets],
            index=[asset.ticker for asset in self.assets],
        )
        self.means = pd.Series(
            [asset.mean_return for asset in self.assets],
            index=[asset.ticker for asset in self.assets],
        )
        self.expected_returns = pd.Series(
            [asset.expected_return for asset in self.assets],
            index=[asset.ticker for asset in self.assets],
        )
        self.returns = get_matrix_returns(self.assets)
        self.covariance_matrix = get_covariance_matrix(self.returns)

    @classmethod
    def from_dict(cls, data: dict, data_provider: DataProvider) -> "Optimization":
        from .optimization_from_dict import create_optimization_from_json

        """
        Alternate constructor that builds Optimization from a dictionary.
        """
        return create_optimization_from_json(data, data_provider)

    def get_var(self) -> float:
        from .compute_var import compute_var

        return compute_var(self)

    def get_efficient_frontier(self, num_points: int):
        from .efficient_frontier import compute_efficient_frontier

        return compute_efficient_frontier(
            expected_returns=self.expected_returns,
            covariance_matrix=self.covariance_matrix,
            num_points=num_points,
        )

    def __repr__(self):
        return f"Optimization(name={self.name}, currency={self.currency}, assets_count={len(self.assets)})"
