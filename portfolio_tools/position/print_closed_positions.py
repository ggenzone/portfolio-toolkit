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
    total_cost = 0
    total_value = 0

    for position in positions:
        value = position.value
        cost = position.cost
        return_percentage = ((value - cost) / cost) * 100 if cost > 0 else 0

        # Add position data to table
        table_data.append(
            {
                "Ticker": position.ticker,
                "Buy Price": position.buy_price,
                "Buy Date": position.buy_date,
                "Sell Price": position.sell_price,
                "Sell Date": position.sell_date,
                "Quantity": position.quantity,
                "Cost": cost,
                "Value": value,
                "Return (%)": return_percentage,
            }
        )

        total_cost += cost
        total_value += value

    # Add total row
    table_data.append(
        {
            "Ticker": "TOTAL",
            "Buy Price": "",
            "Buy Date": "",
            "Sell Price": "",
            "Sell Date": "",
            "Quantity": "",
            "Cost": total_cost,
            "Value": total_value,
            "Return (%)": (
                ((total_value - total_cost) / total_cost) * 100 if total_cost > 0 else 0
            ),
        }
    )

    # Print table
    print(tabulate(table_data, headers="keys", tablefmt="psql", floatfmt=".2f"))
