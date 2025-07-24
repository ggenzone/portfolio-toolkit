import csv
from typing import List

from tabulate import tabulate

from .closed_position import ClosedPosition


def print_closed_positions(positions: List[ClosedPosition], date: str) -> None:
    """
    Prints the closed positions in a tabular format with calculated returns and totals.

    Args:
        positions (List[ClosedPosition]): List of ClosedPosition objects representing closed positions.
        date (str): The date for which the positions are printed.

    Returns:
        None
    """
    print(f"Closed positions as of {date}:")

    # Prepare data for tabulation
    table_data = []

    for position in positions:
        # Add position data to table
        table_data.append(
            {
                "Ticker": position.ticker,
                "Buy Price": position.buy_price,
                "Buy Date": position.buy_date,
                "Sell Price": position.sell_price,
                "Sell Date": position.sell_date,
                "Quantity": position.quantity,
                "Cost": position.cost,
                "Value": position.value,
                "Profit": position.profit,
                "Return (%)": position.return_percentage,
            }
        )
    # Print table
    print(tabulate(table_data, headers="keys", tablefmt="psql", floatfmt=".2f"))


def print_closed_positions_to_csv(
    positions: List[ClosedPosition], date: str, filepath: str
) -> None:
    """
    Saves the closed positions to a CSV file with calculated returns and totals.

    Args:
        positions (List[ClosedPosition]): List of ClosedPosition objects representing closed positions.
        date (str): The date for which the positions are saved.
        filepath (str): The path to the CSV file where data will be saved.

    Returns:
        None
    """
    # Prepare data for CSV
    csv_data = []

    for position in positions:
        # Add position data to CSV data
        csv_data.append(
            {
                "Ticker": position.ticker,
                "Buy Price": position.buy_price,
                "Buy Date": position.buy_date,
                "Sell Price": position.sell_price,
                "Sell Date": position.sell_date,
                "Quantity": position.quantity,
                "Cost": position.cost,
                "Value": position.value,
                "Profit": position.profit,
                "Return (%)": position.return_percentage,
            }
        )

    # Write to CSV file
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "Ticker",
            "Buy Price",
            "Buy Date",
            "Sell Price",
            "Sell Date",
            "Quantity",
            "Cost",
            "Value",
            "Profit",
            "Return (%)",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header with date information
        writer.writeheader()

        # Write data rows
        for row in csv_data:
            writer.writerow(row)

    print(f"Closed positions data saved to: {filepath}")


def print_closed_positions_summary(positions: List[ClosedPosition], date: str) -> None:
    """
    Prints a summary of closed positions with key metrics only.

    Args:
        positions (List[ClosedPosition]): List of ClosedPosition objects representing closed positions.
        date (str): The date for which the positions are printed.

    Returns:
        None
    """
    print(f"Closed positions summary as of {date}:")
    print("-" * 50)

    total_profit = 0
    winning_positions = 0
    losing_positions = 0
    best_return = 0
    worst_return = 0
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

    win_rate = (winning_positions / len(positions)) * 100 if len(positions) > 0 else 0

    print(f"Total positions: {len(positions)}")
    print(f"Winning positions: {winning_positions}")
    print(f"Losing positions: {losing_positions}")
    print(f"Win rate: {win_rate:.1f}%")

    print(f"Total profit: ${total_profit:.2f}")

    print(f"Best performer: {best_ticker} ({best_return:.2f}%)")
    print(f"Worst performer: {worst_ticker} ({worst_return:.2f}%)")
    print("-" * 50)
