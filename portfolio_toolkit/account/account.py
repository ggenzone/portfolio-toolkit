from dataclasses import dataclass, field
from typing import List

import pandas as pd

from .transaction import AccountTransaction


@dataclass
class Account:
    """
    Represents an account with a list of transactions.
    """

    name: str
    currency: str
    transactions: List[AccountTransaction] = field(default_factory=list)

    def add_transaction(self, transaction: AccountTransaction):
        """
        Adds a transaction to the account.

        Args:
            transaction (AccountTransaction): The transaction to add.
        """
        self.transactions.append(transaction)

    def add_transaction_from_dict(self, transaction_dict: dict):
        """
        Adds a transaction to the account from a dictionary.

        Args:
            transaction_dict (dict): Dictionary containing transaction details.
        """
        amount = transaction_dict["total_base"]
        if (
            transaction_dict["type"] == "sell"
            or transaction_dict["type"] == "withdrawal"
        ):
            amount = -amount

        transaction = AccountTransaction(
            transaction_date=transaction_dict["date"],
            transaction_type=transaction_dict["type"],
            amount=amount,
            description=transaction_dict.get("description", None),
        )
        self.add_transaction(transaction)

    def add_transaction_from_assets_dict(self, transaction_dict: dict):
        """
        Adds a transaction to the account from a dictionary.

        Args:
            transaction_dict (dict): Dictionary containing transaction details.
        """
        text = ""
        type = ""
        amount = transaction_dict["total_base"]
        if transaction_dict["type"] == "buy":
            type = "sell"
            text = f"Buy ${transaction_dict['ticker']} asset"
            amount = -amount
        elif transaction_dict["type"] == "sell":
            type = "buy"
            text = f"Sell ${transaction_dict['ticker']} asset"
        elif transaction_dict["type"] == "dividend":
            type = "income"
            text = f"Dividend received for ${transaction_dict['ticker']} asset"
        else:
            raise ValueError(f"Unknown transaction type: {transaction_dict['type']}")

        transaction = AccountTransaction(
            transaction_date=transaction_dict["date"],
            transaction_type=type,
            amount=amount,
            description=text,
        )
        self.add_transaction(transaction)

    def add_transaction_from_split_dict(self, split_dict: dict, amount: float = 0.0):
        """
        Adds a transaction to the account from a stock split dictionary.

        Args:
            split_dict (dict): Dictionary containing split information with keys:
                - date: Split date (str)
                - ticker: Ticker symbol of the asset
                - split_factor: Split ratio as float (e.g., 2.0 for 2:1 split, 0.1 for 1:10 reverse split)
                - amount: Amount of the asset affected by the split (default is 0.0)
        """
        transaction = AccountTransaction(
            transaction_date=split_dict["date"],
            transaction_type="buy",
            amount=amount,
            description=f"Stock split for {split_dict['ticker']} with factor {split_dict['split_factor']}",
        )
        self.add_transaction(transaction)

    @classmethod
    def to_dataframe(cls, account: "Account") -> pd.DataFrame:
        """
        Converts the account transactions to a pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the account transactions.
        """

        return AccountTransaction.to_dataframe(account.transactions)

    def get_amount(self) -> float:
        """
        Calculates the total amount of all transactions in the account.

        Returns:
            float: Total amount of all transactions.
        """
        return sum(tx.amount for tx in self.transactions)

    def sort_transactions(self):
        """
        Sorts the account transactions by date.
        """
        self.transactions.sort(key=lambda x: x.transaction_date)

    def __repr__(self):
        return f"Account(name={self.name}, currency={self.currency}, transactions={self.transactions})"
