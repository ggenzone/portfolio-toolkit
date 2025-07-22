from dataclasses import dataclass, field
from typing import List

from .market_asset import MarketAsset
from .portfolio_asset_transaction import PortfolioAssetTransaction


@dataclass
class PortfolioAsset(MarketAsset):
    transactions: List[PortfolioAssetTransaction] = field(default_factory=list)

    def add_transaction(self, transaction: PortfolioAssetTransaction):
        """
        Adds a transaction to the portfolio asset.
        """
        self.transactions.append(transaction)

    def add_transaction_from_dict(self, transaction_dict: dict):
        """
        Adds a transaction to the account from a dictionary.
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
