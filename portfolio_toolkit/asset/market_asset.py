from dataclasses import dataclass, field
from typing import Dict, List, Optional

import pandas as pd


@dataclass
class MarketAsset:
    ticker: str
    prices: pd.Series
    info: Dict
    currency: Optional[str] = None

    # Campos derivados que no se pasan al constructor
    sector: str = field(init=False)
    country: str = field(init=False)

    def __post_init__(self):
        self.sector = self.info.get("sector", "Unknown")
        self.country = self.info.get("country", "Unknown")
        self.currency = self.currency or self.info.get("currency", "Unknown")

    @classmethod
    def to_dataframe(cls, assets: List["MarketAsset"]) -> pd.DataFrame:
        """Convert a list of MarketAsset objects to a pandas DataFrame."""
        if not assets:
            return pd.DataFrame()

        data = []
        for asset in assets:
            data.append(
                {
                    "ticker": asset.ticker,
                    "sector": asset.sector,
                    "country": asset.country,
                    "currency": asset.currency,
                }
            )

        return pd.DataFrame(data)

    def __repr__(self):
        return (
            f"MarketAsset(ticker={self.ticker}, sector={self.sector}, currency={self.currency}, "
            f"prices_length={len(self.prices)}, info_keys={list(self.info.keys())})"
        )
