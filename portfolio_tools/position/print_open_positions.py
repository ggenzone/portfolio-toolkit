import csv
from typing import List

from tabulate import tabulate

from .valued_position import ValuedPosition


def print_open_positions(positions: List[ValuedPosition]) -> None:
    """
    Prints the positions in a tabular format with calculated returns and totals.

    Args:
        positions (List[ValuedPosition]): List of ValuedPosition objects representing open positions.
        date (str): The date for which the positions are printed.

    Returns:
        None
    """

    # Prepare data for tabulation
    table_data = []
    total_cost = 0
    total_value_base = 0

    for position in positions:
        value_base = position.current_price * position.quantity
        cost = position.cost
        return_percentage = ((value_base - cost) / cost) * 100 if cost > 0 else 0

        # Add position data to table
        table_data.append(
            {
                "Ticker": position.ticker,
                "Price Base": position.buy_price,
                "Cost": cost,
                "Quantity": position.quantity,
                "Value Base": value_base,
                "Return (%)": return_percentage,
            }
        )

        total_cost += cost
        total_value_base += value_base

    # Add total row
    table_data.append(
        {
            "Ticker": "TOTAL",
            "Price Base": "",
            "Cost": total_cost,
            "Quantity": "",
            "Value Base": total_value_base,
            "Return (%)": (
                ((total_value_base - total_cost) / total_cost) * 100
                if total_cost > 0
                else 0
            ),
        }
    )

    # Print table
    print(tabulate(table_data, headers="keys", tablefmt="psql", floatfmt=".2f"))


def print_open_positions_to_csv(positions: List[ValuedPosition], filepath: str) -> None:
    """
    Saves the open positions to a CSV file with calculated returns.

    Args:
        positions (List[ValuedPosition]): List of ValuedPosition objects representing open positions.
        filepath (str): The path to the CSV file where data will be saved.

    Returns:
        None
    """
    # Prepare data for CSV
    csv_data = []

    for position in positions:
        value_base = position.current_price * position.quantity
        cost = position.cost
        return_percentage = ((value_base - cost) / cost) * 100 if cost > 0 else 0

        # Add position data to CSV data
        csv_data.append(
            {
                "Ticker": position.ticker,
                "Price Base": position.buy_price,
                "Cost": cost,
                "Quantity": position.quantity,
                "Value Base": value_base,
                "Return (%)": return_percentage,
            }
        )

    # Write to CSV file
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "Ticker",
            "Price Base",
            "Cost",
            "Quantity",
            "Value Base",
            "Return (%)",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header with date information
        writer.writeheader()

        # Write data rows (without total row as requested)
        for row in csv_data:
            writer.writerow(row)

    print(f"Open positions data saved to: {filepath}")
