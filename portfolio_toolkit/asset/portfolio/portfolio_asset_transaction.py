from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class PortfolioAssetTransaction:
    date: str
    transaction_type: str
    quantity: float
    price: float
    currency: str
    total: float
    exchange_rate: float
    subtotal_base: float
    fees_base: float
    total_base: float

    @classmethod
    def to_dataframe(
        cls, transactions: List["PortfolioAssetTransaction"], ticker: str
    ) -> pd.DataFrame:
        """Convert a list of PortfolioAssetTransaction objects to a pandas DataFrame."""
        if not transactions:
            return pd.DataFrame()

        data = []
        for tx in transactions:
            data.append(
                {
                    "date": tx.date,
                    "ticker": ticker,
                    "type": tx.transaction_type,
                    "quantity": tx.quantity,
                    "price": tx.price,
                    "currency": tx.currency,
                    "total": tx.total,
                    "exchange_rate": tx.exchange_rate,
                    "subtotal_base": tx.subtotal_base,
                    "fees_base": tx.fees_base,
                    "total_base": tx.total_base,
                }
            )

        return pd.DataFrame(data)

    def __repr__(self):
        return (
            f"PortfolioAssetTransaction(date={self.date}, type={self.transaction_type}, quantity={self.quantity}, "
            f"price={self.price}, currency={self.currency}, total={self.total}, exchange_rate={self.exchange_rate}, "
            f"subtotal_base={self.subtotal_base}, fees_base={self.fees_base}, total_base={self.total_base})"
        )
