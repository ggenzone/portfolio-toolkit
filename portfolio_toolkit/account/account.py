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

    def to_list(self) -> List[dict]:
        """
        Converts the account transactions to a list of dictionaries.

        Returns:
            List[dict]: List containing the account transactions.
        """
        return self.transactions.to_list()

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts the account transactions to a pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the account transactions.
        """
        return self.transactions.to_dataframe()

    def export_to_dataframe(self, from_date: str, to_date: str) -> pd.DataFrame:
        """
        Converts the account transactions to a pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the account transactions.
        """
        df = self.transactions.to_dataframe()
        # Filter the DataFrame by the specified date range
        df = df[(df["date"] >= from_date) & (df["date"] <= to_date)]
        return df

    def get_amount(self) -> float:
        """
        Calculates the total amount of all transactions in the account.

        Returns:
            float: Total amount of all transactions.
        """
        return sum(tx.amount for tx in self.transactions)

    def get_amount_at(self, date) -> float:
        """
        Calculates the total amount of all transactions in the account up to a given date.

        Args:
            date: The cutoff date (can be string or date object)

        Returns:
            float: Total amount of all transactions up to the specified date.
        """
        from datetime import datetime

        # Convert date to date object if it's a string
        if isinstance(date, str):
            cutoff_date = datetime.strptime(date, "%Y-%m-%d").date()
        else:  # assume it's already a date object
            cutoff_date = date

        total = 0
        for tx in self.transactions:
            # Convert transaction date to date object for comparison
            if isinstance(tx.transaction_date, str):
                tx_date = datetime.strptime(tx.transaction_date, "%Y-%m-%d").date()
            else:  # assume it's already a date object
                tx_date = tx.transaction_date

            # Include transaction if it's on or before the cutoff date
            if tx_date <= cutoff_date:
                total += tx.amount

        return total

    def sort_transactions(self):
        """
        Sorts the account transactions by date.
        """
        self.transactions.sort(key=lambda x: x.transaction_date)

    def __repr__(self):
        return f"Account(name={self.name}, currency={self.currency}, transactions={self.transactions})"
