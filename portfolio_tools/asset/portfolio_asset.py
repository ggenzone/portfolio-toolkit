from typing import List, Optional

import pandas as pd

from .market_asset import MarketAsset
from .portfolio_asset_transaction import PortfolioAssetTransaction


class PortfolioAsset(MarketAsset):
    def __init__(
        self,
        ticker: str,
        prices: pd.Series,
        info: dict,
        currency: Optional[str] = None,
        transactions: Optional[List[PortfolioAssetTransaction]] = None,
    ):
        """
        Represents a portfolio asset, extending MarketAsset with transactions.

        Args:
            ticker (str): The ticker symbol of the asset.
            prices (pd.Series): Historical price data for the asset.
            info (dict): Additional information about the asset (e.g., from a data provider).
            currency (Optional[str]): The currency for the asset. If None, it is derived from the info.
            transactions (Optional[List[PortfolioAssetTransaction]]): List of transactions for the asset.
        """
        super().__init__(ticker, prices, info, currency)
        self.transactions = transactions or []

    def add_transaction(self, transaction: PortfolioAssetTransaction):
        """
        Adds a transaction to the portfolio asset.

        Args:
            transaction (PortfolioAssetTransaction): The transaction to add.
        """
        self.transactions.append(transaction)

    def add_transaction_from_dict(self, transaction_dict: dict):
        """
        Adds a transaction to the account from a dictionary.

        Args:
            transaction_dict (dict): Dictionary containing transaction details.
        """
        transaction = PortfolioAssetTransaction(
            date=transaction_dict["date"],
            transaction_type=transaction_dict["type"],
            quantity=transaction_dict["quantity"],
            price=transaction_dict["price"],
            currency=transaction_dict["currency"],
            total=transaction_dict["total"],
            exchange_rate=transaction_dict["exchange_rate"],
            subtotal_base=transaction_dict["subtotal_base"],
            fees_base=transaction_dict["fees_base"],
            total_base=transaction_dict["total_base"],
        )
        self.add_transaction(transaction)

    def __repr__(self):
        return (
            f"PortfolioAsset(ticker={self.ticker}, sector={self.sector}, currency={self.currency}, "
            f"prices_length={len(self.prices)}, transactions_count={len(self.transactions)}, "
            f"info_keys={list(self.info.keys())})"
        )
