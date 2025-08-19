from dataclasses import dataclass
from datetime import date
from typing import List, Optional

import pandas as pd


@dataclass
class AccountTransaction:
    """
    Represents a transaction in an account.
    """

    transaction_date: date
    transaction_type: str
    amount: float
    description: Optional[str] = None

    def __post_init__(self):
        allowed_types = {"buy", "sell", "deposit", "withdrawal", "income", "adjustment"}
        if self.transaction_type not in allowed_types:
            raise ValueError(f"Invalid transaction type: {self.transaction_type}")

    def to_list(self) -> List[dict]:
        """Convert a list of AccountTransaction objects to a list of dictionaries."""

        data = []
        for tx in self.transactions:
            data.append(
                {
                    "date": tx.transaction_date,
                    "type": tx.transaction_type,
                    "amount": tx.amount,
                    "description": tx.description,
                }
            )

        return data

    def to_dataframe(self) -> pd.DataFrame:
        """Convert the account transactions to a pandas DataFrame."""

        data = self.to_list()
        return pd.DataFrame(data)

    def __repr__(self):
        return (
            f"AccountTransaction(date={self.transaction_date}, "
            f"type={self.transaction_type}, amount={self.amount}, "
            f"description={self.description})"
        )
