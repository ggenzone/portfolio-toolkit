from typing import List

from .transaction import AccountTransaction


class Account:
    def __init__(self, name: str, currency: str):
        """
        Represents an account with a list of transactions.

        Args:
            name (str): The name of the account.
            currency (str): The currency of the account.
        """
        self.name = name
        self.currency = currency
        self.transactions: List[AccountTransaction] = []

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

    def __repr__(self):
        return f"Account(name={self.name}, currency={self.currency}, transactions={self.transactions})"
