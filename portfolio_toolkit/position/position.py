from dataclasses import dataclass, field
from typing import List

import pandas as pd


@dataclass
class Position:
    ticker: str
    buy_price: float
    quantity: float
    cost: float = field(init=False)

    def __post_init__(self):
        self.cost = self.buy_price * self.quantity

    @classmethod
    def to_list(cls, positions: List["Position"]) -> List[dict]:
        """Convert a list of Position objects to a list of dictionaries."""
        if not positions:
            return []

        data = []
        for position in positions:
            data.append(
                {
                    "ticker": position.ticker,
                    "buy_price": position.buy_price,
                    "quantity": position.quantity,
                    "cost": position.cost,
                }
            )

        return data

    @classmethod
    def to_dataframe(cls, positions: List["Position"]) -> pd.DataFrame:
        """Convert a list of Position objects to a pandas DataFrame."""

        data = cls.to_list(positions)

        return pd.DataFrame(data)

    def __repr__(self):
        return (
            f"Position(ticker={self.ticker}, buy_price={self.buy_price}, "
            f"quantity={self.quantity}, cost={self.cost})"
        )
