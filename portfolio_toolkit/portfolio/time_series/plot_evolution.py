import pandas as pd

from portfolio_toolkit.plot.line_chart_data import LineChartData

from .portfolio_time_series import PortfolioTimeSeries


def plot_portfolio_evolution(portfolio: PortfolioTimeSeries) -> LineChartData:
    """Plot open positions in the portfolio"""

    portfolio_data = portfolio.portfolio_timeseries

    if portfolio_data is None or portfolio_data.empty:
        raise ValueError("Portfolio DataFrame is not available.")

    df_pivot = portfolio_data.pivot_table(
        index="Date", columns="Ticker", values="Value_Base", aggfunc="sum", fill_value=0
    )
    df_pivot.sort_index(inplace=True)

    dates = pd.to_datetime(df_pivot.index)
    values = df_pivot.sum(axis=1).values

    line_data = LineChartData(
        title="Portfolio Evolution",
        x_data=dates,
        y_data=[values],
        labels=["Portfolio Value"],
        xlabel="Date",
        ylabel="Value ($)",
        colors=["green"],
    )

    return line_data
