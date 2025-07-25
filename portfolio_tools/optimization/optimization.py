from dataclasses import dataclass
from typing import List

from portfolio_tools.asset.optimization_asset import OptimizationAsset
from portfolio_tools.data_provider.data_provider import DataProvider


@dataclass
class Optimization:
    """
    Class to represent and manage an asset optimization.
    """

    name: str
    currency: str
    assets: List[OptimizationAsset]
    data_provider: DataProvider

    def __repr__(self):
        return f"Optimization(name={self.name}, currency={self.currency}, assets_count={len(self.assets)})"
