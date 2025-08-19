from typing import Any, Dict, Iterator, List

import pandas as pd

from portfolio_toolkit.asset import PortfolioAsset

from .closed_position import ClosedPosition


class ClosedPositionList:
    def __init__(self, positions: List[ClosedPosition]):
        self.positions = positions

    def __iter__(self) -> Iterator[ClosedPosition]:
        return iter(self.positions)

    def __len__(self) -> int:
        return len(self.positions)

    def __getitem__(self, idx):
        return self.positions[idx]

    @classmethod
    def from_portfolio(
        cls, portfolio: List[PortfolioAsset], from_date: str, to_date: str
    ) -> "ClosedPositionList":
        """
        Create ClosedPositionList from a portfolio.
        """
        from .list_from_portfolio import get_closed_positions

        return get_closed_positions(portfolio, from_date, to_date)

    def get_stats(self, date: str) -> Dict[str, Any]:
        from .get_closed_positions_stats import get_closed_positions_stats

        return get_closed_positions_stats(self, date)

    def to_list(self) -> List[dict]:
        """Convert to a list of dictionaries."""
        return ClosedPosition.to_list(self.positions)

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to a pandas DataFrame."""
        return ClosedPosition.to_dataframe(self.positions)
