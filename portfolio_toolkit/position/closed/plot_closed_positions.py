from collections import defaultdict
from datetime import datetime
from typing import List

from portfolio_toolkit.plot.bar_chart_data import BarChartData

from .closed_position import ClosedPosition


def plot_closed_positions(closed_positions: List[ClosedPosition]) -> BarChartData:
    """Plot closed positions grouped by month of sale"""

    # Group by month and sum profits
    monthly_profits = defaultdict(float)

    for pos in closed_positions:
        # Parse sell_date and extract year-month
        if isinstance(pos.sell_date, str):
            # Assuming date format is YYYY-MM-DD
            sell_date = datetime.strptime(pos.sell_date, "%Y-%m-%d")
        else:
            sell_date = pos.sell_date

        # Create month key (YYYY-MM format)
        month_key = sell_date.strftime("%Y-%m")
        monthly_profits[month_key] += pos.profit

    # Sort months chronologically
    sorted_months = sorted(monthly_profits.keys())

    # Prepare data for plotting
    labels = sorted_months
    values = [monthly_profits[month] for month in sorted_months]

    # Color bars: green for positive profits, red for negative
    colors = ["green" if profit >= 0 else "red" for profit in values]

    bar_data = BarChartData(
        title="Monthly Profit from Closed Positions",
        labels=labels,
        values=values,
        xlabel="Month",
        ylabel="Profit ($)",
        colors=colors,
    )

    return bar_data


def plot_closed_positions_by_ticker(
    closed_positions: List[ClosedPosition],
) -> BarChartData:
    """Plot closed positions grouped by ticker"""

    # Group by ticker and sum profits
    ticker_profits = defaultdict(float)

    for pos in closed_positions:
        ticker_profits[pos.ticker] += pos.profit

    # Sort by profit (descending)
    sorted_tickers = sorted(ticker_profits.items(), key=lambda x: x[1], reverse=True)

    labels = [ticker for ticker, _ in sorted_tickers]
    values = [profit for _, profit in sorted_tickers]

    # Color bars: green for positive profits, red for negative
    colors = ["green" if profit >= 0 else "red" for profit in values]

    bar_data = BarChartData(
        title="Profit by Ticker (Closed Positions)",
        labels=labels,
        values=values,
        xlabel="Ticker",
        ylabel="Profit ($)",
        colors=colors,
    )

    return bar_data


def plot_closed_positions_count_by_month(
    closed_positions: List[ClosedPosition],
) -> BarChartData:
    """Plot count of closed positions by month"""

    # Group by month and count positions
    monthly_counts = defaultdict(int)

    for pos in closed_positions:
        # Parse sell_date and extract year-month
        if isinstance(pos.sell_date, str):
            sell_date = datetime.strptime(pos.sell_date, "%Y-%m-%d")
        else:
            sell_date = pos.sell_date

        month_key = sell_date.strftime("%Y-%m")
        monthly_counts[month_key] += 1

    # Sort months chronologically
    sorted_months = sorted(monthly_counts.keys())

    labels = sorted_months
    values = [monthly_counts[month] for month in sorted_months]

    bar_data = BarChartData(
        title="Number of Positions Closed by Month",
        labels=labels,
        values=values,
        xlabel="Month",
        ylabel="Number of Positions",
        colors=["steelblue"] * len(values),
    )

    return bar_data
