from dataclasses import dataclass, field
from typing import List

import pandas as pd

from .position import Position


@dataclass
class ValuedPosition(Position):
    current_price: float
    sector: str
    country: str
    value: float = field(init=False)

    def __post_init__(self):
        super().__post_init__()  # Calcula cost
        self.value = self.current_price * self.quantity

    @classmethod
    def to_dataframe(cls, positions: List["ValuedPosition"]) -> pd.DataFrame:
        """Convert a list of Position objects to a pandas DataFrame."""
        if not positions:
            return pd.DataFrame()

        data = []
        for position in positions:
            data.append(
                {
                    "ticker": position.ticker,
                    "buy_price": position.buy_price,
                    "quantity": position.quantity,
                    "cost": position.cost,
                    "current_price": position.current_price,
                    "value": position.value,
                    "sector": position.sector,
                    "country": position.country,
                }
            )

        return pd.DataFrame(data)

    def __repr__(self):
        return (
            f"ValuedPosition(ticker={self.ticker}, buy_price={self.buy_price}, quantity={self.quantity}, "
            f"cost={self.cost}, current_price={self.current_price}, value={self.value})"
        )
