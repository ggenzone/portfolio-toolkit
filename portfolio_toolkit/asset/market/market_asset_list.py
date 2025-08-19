from typing import Iterator, List

import pandas as pd

from .market_asset import MarketAsset


class MarketAssetList:
    def __init__(self, assets: List[MarketAsset]):
        self.assets = assets

    def __iter__(self) -> Iterator[MarketAsset]:
        return iter(self.assets)

    def __len__(self) -> int:
        return len(self.assets)

    def __getitem__(self, idx):
        return self.assets[idx]

    def to_list(self) -> List[dict]:
        """Convert to a list of dictionaries."""
        if not self.assets:
            return []

        return [asset.to_dict() for asset in self.assets]

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to a pandas DataFrame."""

        return pd.DataFrame(self.to_list())
