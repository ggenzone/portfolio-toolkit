from datetime import date
from typing import Optional


class AccountTransaction:
    def __init__(
        self,
        transaction_date: date,
        transaction_type: str,
        amount: float,
        description: Optional[str] = None,
    ):
        """
        Represents a transaction in an account.

        Args:
            transaction_date (date): The date of the transaction.
            transaction_type (str): The type of transaction ('buy', 'sell', 'deposit', 'withdrawal').
            amount (float): The amount involved in the transaction.
            description (Optional[str]): Additional details about the transaction.
        """
        if transaction_type not in {"buy", "sell", "deposit", "withdrawal"}:
            raise ValueError(f"Invalid transaction type: {transaction_type}")

        self.transaction_date = transaction_date
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description

    def __repr__(self):
        return f"AccountTransaction(date={self.transaction_date}, type={self.transaction_type}, amount={self.amount}, description={self.description})"
