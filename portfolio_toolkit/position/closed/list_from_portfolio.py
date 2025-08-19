from typing import List

from portfolio_toolkit.asset import PortfolioAsset

from .closed_position import ClosedPosition
from .closed_position_list import ClosedPositionList


def get_closed_positions(
    assets: List[PortfolioAsset], from_date: str, to_date: str
) -> ClosedPositionList:
    """
    Calculates all closed positions for multiple assets using FIFO logic up to a specific date.

    Args:
        assets (List[PortfolioAsset]): List of PortfolioAsset objects containing transactions.
        date (str): The date up to which closed positions are calculated (YYYY-MM-DD).

    Returns:
        ClosedPositionList: List of all ClosedPosition objects from all assets.
    """
    all_closed_positions: List[ClosedPosition] = []

    for asset in assets:
        asset_closed_positions = get_asset_closed_positions(asset, from_date, to_date)
        all_closed_positions.extend(asset_closed_positions)

    return ClosedPositionList(all_closed_positions)


def get_asset_closed_positions(
    asset: PortfolioAsset, from_date: str, to_date: str
) -> List[ClosedPosition]:
    """
    Calculates all closed positions for an asset using FIFO logic up to a specific date.
    Each 'sell' transaction closes positions from the oldest 'buy' transactions.

    Args:
        asset (dict): Asset dictionary containing transactions.
        date (str): The date up to which closed positions are calculated (YYYY-MM-DD).

    Returns:
        List[ClosedPosition]: List of ClosedPosition objects representing closed positions.
    """
    transactions = sorted(
        [tx for tx in asset.transactions if tx.date <= to_date], key=lambda x: x.date
    )
    ticker = asset.ticker

    # Stack to track open buy positions (FIFO)
    open_positions = []
    closed_positions: List[ClosedPosition] = []

    for transaction in transactions:
        if transaction.transaction_type == "buy":
            # Add to open positions
            open_positions.append(
                {
                    "date": transaction.date,
                    "quantity": transaction.quantity,
                    "total_base": transaction.total_base,
                    "price": (
                        transaction.total_base / transaction.quantity
                        if transaction.quantity > 0
                        else 0
                    ),
                }
            )

        elif transaction.transaction_type == "sell":
            # Close positions using FIFO
            remaining_to_sell = transaction.quantity
            sell_price = (
                transaction.total_base / transaction.quantity
                if transaction.quantity > 0
                else 0
            )

            while remaining_to_sell > 0 and open_positions:
                oldest_position = open_positions[0]

                # Determine how much to close from this position
                quantity_to_close = min(remaining_to_sell, oldest_position["quantity"])

                # Create ClosedPosition object
                closed_position = ClosedPosition(
                    ticker=ticker,
                    buy_price=oldest_position["price"],
                    quantity=quantity_to_close,
                    buy_date=oldest_position["date"],
                    sell_price=sell_price,
                    sell_date=transaction.date,
                )

                # Add to closed positions list
                closed_positions.append(closed_position)

                # Update remaining quantities
                remaining_to_sell -= quantity_to_close
                oldest_position["quantity"] -= quantity_to_close

                # Remove position if fully closed
                if oldest_position["quantity"] == 0:
                    open_positions.pop(0)

    # Filter closed positions by from_date
    filtered_closed_positions = [
        pos for pos in closed_positions if pos.sell_date >= from_date
    ]

    return filtered_closed_positions
