from typing import List

from portfolio_tools.asset.portfolio_asset import PortfolioAsset
from portfolio_tools.position.get_asset_open_positions import get_asset_open_positions

from .valued_position import ValuedPosition


def get_open_positions(assets: List[PortfolioAsset], date: str) -> List[ValuedPosition]:
    """
    Gets the open positions of a portfolio as of a given date and returns them as a list of ValuedPosition objects.

    Args:
        assets (List[PortfolioAsset]): List of PortfolioAsset objects containing transactions.
        date (str): The date up to which the positions are calculated (YYYY-MM-DD).

    Returns:
        List[ValuedPosition]: A list of ValuedPosition objects representing open positions.
    """
    positions: List[ValuedPosition] = []

    for asset in assets:
        ticker = asset.ticker
        position = get_asset_open_positions(asset, date)

        if position.quantity != 0:  # Only include positions with non-zero quantity
            valued_position = ValuedPosition(
                ticker=ticker,
                buy_price=position.buy_price,
                quantity=position.quantity,
                current_price=position.current_price,
            )

            positions.append(valued_position)

    return positions
