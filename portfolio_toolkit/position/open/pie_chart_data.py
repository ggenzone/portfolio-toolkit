from collections import defaultdict

import matplotlib.pyplot as plt

from portfolio_toolkit.plot.pie_chart_data import PieChartData

from .open_position_list import OpenPositionList


def get_pie_chart_data(
    open_positions: OpenPositionList, group_by: str = "Ticker"
) -> PieChartData:
    """Plot open positions in the portfolio"""

    if group_by not in ["Ticker", "Country", "Sector"]:
        raise ValueError("group_by must be either 'Ticker', 'Country' or 'Sector'")

    labels = []
    values = []
    if group_by == "Country":
        # Group by country and sum quantities
        country_quantities = defaultdict(float)
        for pos in open_positions:
            country_quantities[pos.country] += pos.value

        labels = list(country_quantities.keys())
        values = list(country_quantities.values())

    elif group_by == "Sector":
        # Group by sector and sum quantities
        sector_quantities = defaultdict(float)
        for pos in open_positions:
            sector_quantities[pos.sector] += pos.value

        labels = list(sector_quantities.keys())
        values = list(sector_quantities.values())

    elif group_by == "Ticker":
        # Group by ticker
        labels = [pos.ticker for pos in open_positions]
        values = [pos.value for pos in open_positions]

    # Prepare data for plotting
    pie_data = PieChartData(
        title="Open Positions",
        labels=labels,
        values=values,
        colors=plt.cm.tab20.colors[: len(values)],
    )

    return pie_data
