from typing import Iterator, List

import pandas as pd

from portfolio_toolkit.asset import PortfolioAsset
from portfolio_toolkit.plot.pie_chart_data import PieChartData

from .open_position import OpenPosition


class OpenPositionList:
    def __init__(self, positions: List[OpenPosition]):
        self.positions = positions

    def __iter__(self) -> Iterator[OpenPosition]:
        return iter(self.positions)

    def __len__(self) -> int:
        return len(self.positions)

    def __getitem__(self, idx):
        return self.positions[idx]

    @classmethod
    def from_portfolio(
        cls, portfolio: List[PortfolioAsset], date: str
    ) -> "OpenPositionList":
        """
        Create OpenPositionList from a portfolio.
        """
        from .list_from_portfolio import get_open_positions

        return get_open_positions(portfolio, date)

    def get_pie_chart_data(self, group_by: str = "Ticker") -> PieChartData:
        from .pie_chart_data import get_pie_chart_data

        return get_pie_chart_data(self, group_by=group_by)

    def to_list(self) -> List[dict]:
        """Convert to a list of dictionaries."""
        return OpenPosition.to_list(self.positions)

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to a pandas DataFrame."""
        return OpenPosition.to_dataframe(self.positions)
