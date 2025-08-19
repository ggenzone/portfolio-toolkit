from dataclasses import dataclass
from typing import Any, Dict

import pandas as pd

from ..portfolio import Portfolio


@dataclass
class PortfolioStats:
    """
    Portfolio statistics dataclass containing all financial metrics and data for a given period.

    Attributes:
        realized_profit (float): Total profit/loss from closed positions
        unrealized_profit (float): Unrealized gains/losses from current open positions
        initial_valuation (float): Portfolio valuation at start of period
        final_valuation (float): Portfolio valuation at end of period
        incomes (float): Total income transactions in period
        deposits (float): Total deposit transactions in period
        withdrawals (float): Total withdrawal transactions in period
        commission (float): Total commission fees (currently 0.0)
        closed_positions_stats (Dict[str, Any]): Statistics about closed positions
        closed_positions (pd.DataFrame): DataFrame of closed positions
        open_positions (pd.DataFrame): DataFrame of current open positions
        transactions (pd.DataFrame): DataFrame of account transactions
    """

    # Financial metrics
    realized_profit: float
    unrealized_profit: float
    initial_cash: float
    final_cash: float
    initial_valuation: float
    final_valuation: float

    # Transaction summaries
    incomes: float
    deposits: float
    withdrawals: float
    commission: float

    # Detailed statistics
    closed_positions_stats: Dict[str, Any]

    # DataFrames
    closed_positions: pd.DataFrame
    open_positions: pd.DataFrame
    transactions: pd.DataFrame

    @classmethod
    def from_portfolio(cls, portfolio: Portfolio, year: str) -> "PortfolioStats":
        """
        Alternate constructor that builds PortfolioStats from a Portfolio and year.
        """
        from .stats_from_portfolio import stats_from_portfolio

        return stats_from_portfolio(portfolio, year)

    @property
    def total_profit(self) -> float:
        """Total profit including both realized and unrealized gains"""
        return self.realized_profit + self.unrealized_profit

    @property
    def valuation_change(self) -> float:
        """Change in portfolio valuation from start to end of period"""
        return self.final_valuation - self.initial_valuation

    @property
    def net_cash_flow(self) -> float:
        """Net cash flow (deposits - withdrawals + incomes)"""
        return self.deposits - self.withdrawals + self.incomes

    @property
    def return_percentage(self) -> float:
        """Portfolio return percentage for the period"""
        if self.initial_valuation > 0:
            return (self.valuation_change / self.initial_valuation) * 100
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert PortfolioStats to dictionary for backward compatibility"""
        return {
            "realized_profit": self.realized_profit,
            "unrealized_profit": self.unrealized_profit,
            "initial_cash": self.initial_cash,
            "final_cash": self.final_cash,
            "initial_valuation": self.initial_valuation,
            "final_valuation": self.final_valuation,
            "incomes": self.incomes,
            "deposits": self.deposits,
            "withdrawals": self.withdrawals,
            "commission": self.commission,
            "closed_positions_stats": self.closed_positions_stats,
            "closed_positions": self.closed_positions,
            "open_positions": self.open_positions,
            "transactions": self.transactions,
            # Additional computed properties
            "total_profit": self.total_profit,
            "valuation_change": self.valuation_change,
            "net_cash_flow": self.net_cash_flow,
            "return_percentage": self.return_percentage,
        }
