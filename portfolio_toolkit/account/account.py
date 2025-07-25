from dataclasses import dataclass, field
from typing import List

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
        transaction = AccountTransaction(
            transaction_date=transaction_dict["date"],
            transaction_type=transaction_dict["type"],
            amount=transaction_dict["total_base"],
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
        if transaction_dict["type"] == "buy":
            type = "sell"
            text = f"Sell ${transaction_dict['ticker']} asset"
        elif transaction_dict["type"] == "sell":
            type = "buy"
            text = f"Buy ${transaction_dict['ticker']} asset"
        elif transaction_dict["type"] == "dividend":
            type = "income"
            text = f"Dividend received for ${transaction_dict['ticker']} asset"
        else:
            raise ValueError(f"Unknown transaction type: {transaction_dict['type']}")

        transaction = AccountTransaction(
            transaction_date=transaction_dict["date"],
            transaction_type=type,
            amount=transaction_dict["total_base"],
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

    def __repr__(self):
        return f"Account(name={self.name}, currency={self.currency}, transactions={self.transactions})"
