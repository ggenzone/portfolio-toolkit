from dataclasses import dataclass
from typing import List

from portfolio_toolkit.account.account import Account
from portfolio_toolkit.asset.portfolio.portfolio_asset import PortfolioAsset
from portfolio_toolkit.data_provider.data_provider import DataProvider


@dataclass
class Portfolio:
    name: str
    currency: str
    assets: List[PortfolioAsset]
    data_provider: DataProvider
    account: Account
    start_date: str  # = field(init=False)

    def __post_init__(self):
        self.account.sort_transactions()

    # def __post_init__(self):
    #    # Determina la fecha más antigua de las transacciones de todos los activos
    #    all_dates = []
    #    for asset in self.assets:
    #        for tx in asset.transactions:
    #            all_dates.append(tx.date)

    #    if all_dates:
    #        self.start_date = min(all_dates)
    #    else:
    #        self.start_date = "N/A"  # o lanzar una excepción si es requerido

    @classmethod
    def from_dict(cls, data: dict, data_provider: DataProvider) -> "Portfolio":
        from .portfolio_from_dict import portfolio_from_dict

        """
        Alternate constructor that builds PortfolioStats from a Portfolio and year.
        """
        return portfolio_from_dict(data, data_provider)

    def __repr__(self):
        return (
            f"Portfolio(name={self.name}, currency={self.currency}, "
            f"assets={len(self.assets)}, start_date={self.start_date}, "
            f"data_provider={type(self.data_provider).__name__}, "
            f"account={self.account})"
        )

    def get_stats(self, year: str) -> "PortfolioStats":
        """
        Returns PortfolioStats for the given year.
        """
        from .stats.portfolio_stats import PortfolioStats

        return PortfolioStats.from_portfolio(self, year)

    def get_time_series(self) -> "PortfolioTimeSeries":
        """
        Returns a PortfolioTimeSeries for the given portfolio.
        """
        from .time_series.portfolio_time_series import PortfolioTimeSeries

        return PortfolioTimeSeries.from_portfolio(self)

    def get_open_positions(self, date: str) -> "OpenPositionList":
        """
        Returns OpenPositionList for the given date.
        """
        from portfolio_toolkit.position.open.open_position_list import OpenPositionList

        return OpenPositionList.from_portfolio(self.assets, date)

    def get_closed_positions(
        self, from_date: str, to_date: str
    ) -> "ClosedPositionList":
        """
        Returns ClosedPositionList for the given date.
        """
        from portfolio_toolkit.position.closed.closed_position_list import (
            ClosedPositionList,
        )

        return ClosedPositionList.from_portfolio(self.assets, from_date, to_date)
