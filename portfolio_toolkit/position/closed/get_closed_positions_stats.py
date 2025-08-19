from typing import Any, Dict

from .closed_position_list import ClosedPositionList


def get_closed_positions_stats(
    positions: ClosedPositionList, date: str
) -> Dict[str, Any]:
    """
    Calculates a summary of closed positions with key metrics.

    Args:
        positions (List[ClosedPosition]): List of ClosedPosition objects representing closed positions.
        date (str): The date for which the positions are calculated.

    Returns:
        Dict[str, Any]: Dictionary containing summary metrics:
            - date: Reference date
            - total_positions: Total number of positions
            - winning_positions: Number of profitable positions
            - losing_positions: Number of unprofitable positions
            - win_rate: Win rate percentage
            - total_profit: Total profit/loss
            - best_return: Best return percentage
            - best_ticker: Ticker with best performance
            - worst_return: Worst return percentage
            - worst_ticker: Ticker with worst performance
    """
    if not positions:
        return {
            "date": date,
            "total_positions": 0,
            "winning_positions": 0,
            "losing_positions": 0,
            "win_rate": 0.0,
            "total_profit": 0.0,
            "best_return": 0.0,
            "best_ticker": "",
            "worst_return": 0.0,
            "worst_ticker": "",
        }

    total_profit = 0
    winning_positions = 0
    losing_positions = 0
    best_return = float("-inf")
    worst_return = float("inf")
    best_ticker = ""
    worst_ticker = ""

    for position in positions:
        return_percentage = position.return_percentage
        total_profit += position.profit

        if return_percentage > 0:
            winning_positions += 1
        elif return_percentage < 0:
            losing_positions += 1

        if return_percentage > best_return:
            best_return = return_percentage
            best_ticker = position.ticker

        if return_percentage < worst_return:
            worst_return = return_percentage
            worst_ticker = position.ticker

    win_rate = (winning_positions / len(positions)) * 100

    return {
        "date": date,
        "total_positions": len(positions),
        "winning_positions": winning_positions,
        "losing_positions": losing_positions,
        "win_rate": win_rate,
        "total_profit": total_profit,
        "best_return": best_return,
        "best_ticker": best_ticker,
        "worst_return": worst_return,
        "worst_ticker": worst_ticker,
    }


def print_closed_positions_summary(positions: ClosedPositionList, date: str) -> None:
    """
    Prints a summary of closed positions with key metrics only.

    This function uses get_closed_positions_summary() and formats the output.

    Args:
        positions (List[ClosedPosition]): List of ClosedPosition objects representing closed positions.
        date (str): The date for which the positions are printed.

    Returns:
        None
    """
    summary = get_closed_positions_stats(positions, date)

    print(f"Closed positions summary as of {summary['date']}:")
    print("-" * 50)
    print(f"Total positions: {summary['total_positions']}")
    print(f"Winning positions: {summary['winning_positions']}")
    print(f"Losing positions: {summary['losing_positions']}")
    print(f"Win rate: {summary['win_rate']:.1f}%")
    print(f"Total profit: ${summary['total_profit']:.2f}")
    print(f"Best performer: {summary['best_ticker']} ({summary['best_return']:.2f}%)")
    print(
        f"Worst performer: {summary['worst_ticker']} ({summary['worst_return']:.2f}%)"
    )
    print("-" * 50)
