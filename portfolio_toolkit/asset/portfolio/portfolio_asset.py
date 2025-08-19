from dataclasses import dataclass, field
from typing import List, Optional

import pandas as pd

from portfolio_toolkit.data_provider.data_provider import DataProvider

from ..market import MarketAsset
from .portfolio_asset_transaction import PortfolioAssetTransaction


@dataclass
class PortfolioAsset(MarketAsset):
    transactions: List[PortfolioAssetTransaction] = field(default_factory=list)

    @classmethod
    def from_ticker(
        cls, data_provider: DataProvider, ticker: str, currency: Optional[str] = None
    ) -> "PortfolioAsset":
        """Create a PortfolioAsset from a ticker."""

        from .asset_from_dict import create_portfolio_asset

        return create_portfolio_asset(data_provider, ticker, currency)

    @classmethod
    def to_dataframe(cls, assets: List["PortfolioAsset"]) -> pd.DataFrame:
        """Convert a list of PortfolioAsset objects to a pandas DataFrame."""
        data = pd.DataFrame()
        if not assets:
            return data

        for asset in assets:
            transactions = PortfolioAssetTransaction.to_dataframe(
                asset.transactions, asset.ticker
            )
            data = pd.concat([data, transactions], ignore_index=True)

        # Only sort if columns exist
        if not data.empty and "date" in data.columns and "ticker" in data.columns:
            data.sort_values(by=["date", "ticker"], inplace=True)
            data.reset_index(drop=True, inplace=True)
        return data

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

    def add_split(self, split_dict: dict) -> float:
        """
        Adds a stock split to the portfolio asset by simulating sell all + buy equivalent.
        Creates a sell transaction for all held shares and a buy transaction for split-adjusted quantity.

        Args:
            split_dict: Dictionary containing split information with keys:
                - date: Split date (str)
                - split_factor: Split ratio as float (e.g., 2.0 for 2:1 split, 0.1 for 1:10 reverse split)

        Returns:
            float: Cash amount to be added to account due to fractional shares sold
                   (only applies to reverse splits where shares are lost)
        """
        from portfolio_toolkit.position.open.list_from_portfolio import (
            get_asset_open_positions,
        )

        split_date = split_dict["date"]
        split_factor = split_dict["split_factor"]

        # Get open positions at split date (day before split)
        open_positions = get_asset_open_positions(self, split_date)

        if not open_positions or open_positions.quantity == 0:
            # No open positions to split
            return 0.0

        # Calculate total quantity held and average cost
        total_quantity = open_positions.quantity
        total_cost_base = open_positions.cost
        average_cost_per_share = (
            total_cost_base / total_quantity if total_quantity > 0 else 0
        )

        # Calculate new quantities after split
        exact_new_quantity = total_quantity * split_factor
        new_total_quantity = int(exact_new_quantity)  # Integer part only
        fractional_shares = (
            exact_new_quantity - new_total_quantity
        )  # Shares that become cash

        # Calculate prices and costs
        new_price_per_share = average_cost_per_share / split_factor
        new_total_cost_base = new_total_quantity * new_price_per_share

        # Calculate cash from fractional shares (at post-split price)
        cash_from_fractional_shares = fractional_shares * new_price_per_share

        # Create sell transaction for all current holdings
        sell_transaction = PortfolioAssetTransaction(
            date=split_date,
            transaction_type="sell",
            quantity=total_quantity,
            price=average_cost_per_share,
            currency=self.currency,
            total=total_cost_base,
            exchange_rate=1.0,  # Assuming same currency
            subtotal_base=total_cost_base,
            fees_base=0.0,  # No fees for split
            total_base=total_cost_base,
        )

        # Create buy transaction for split-adjusted quantity (only whole shares)
        buy_transaction = PortfolioAssetTransaction(
            date=split_date,
            transaction_type="buy",
            quantity=new_total_quantity,
            price=new_price_per_share,
            currency=self.currency,
            total=new_total_cost_base,
            exchange_rate=1.0,  # Assuming same currency
            subtotal_base=new_total_cost_base,
            fees_base=0.0,  # No fees for split
            total_base=new_total_cost_base,
        )

        # Add transactions to the asset
        self.add_transaction(sell_transaction)
        self.add_transaction(buy_transaction)

        # Sort transactions by date to maintain chronological order
        self.transactions.sort(key=lambda x: x.date)

        # Return cash amount from fractional shares
        return cash_from_fractional_shares

    def __repr__(self):
        return (
            f"PortfolioAsset(ticker={self.ticker}, sector={self.sector}, currency={self.currency}, "
            f"prices_length={len(self.prices)}, transactions_count={len(self.transactions)}, "
            f"info_keys={list(self.info.keys())})"
        )
