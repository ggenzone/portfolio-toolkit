from typing import List

from portfolio_toolkit.asset.portfolio_asset import PortfolioAsset
from portfolio_toolkit.position.get_asset_closed_positions import (
    get_asset_closed_positions,
)

from .closed_position import ClosedPosition


def get_closed_positions(
    assets: List[PortfolioAsset], from_date: str, to_date: str
) -> List[ClosedPosition]:
    """
    Calculates all closed positions for multiple assets using FIFO logic up to a specific date.

    Args:
        assets (List[PortfolioAsset]): List of PortfolioAsset objects containing transactions.
        date (str): The date up to which closed positions are calculated (YYYY-MM-DD).

    Returns:
        List[ClosedPosition]: List of all ClosedPosition objects from all assets.
    """
    all_closed_positions: List[ClosedPosition] = []

    for asset in assets:
        asset_closed_positions = get_asset_closed_positions(asset, from_date, to_date)
        all_closed_positions.extend(asset_closed_positions)

    return all_closed_positions
