from dataclasses import dataclass
from datetime import date
from typing import Optional


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
        allowed_types = {"buy", "sell", "deposit", "withdrawal", "income"}
        if self.transaction_type not in allowed_types:
            raise ValueError(f"Invalid transaction type: {self.transaction_type}")

    def __repr__(self):
        return (
            f"AccountTransaction(date={self.transaction_date}, "
            f"type={self.transaction_type}, amount={self.amount}, "
            f"description={self.description})"
        )
