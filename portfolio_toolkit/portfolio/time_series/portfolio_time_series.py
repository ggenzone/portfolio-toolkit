from dataclasses import dataclass, field

import pandas as pd

from portfolio_toolkit.plot.line_chart_data import LineChartData
from portfolio_toolkit.position.open.list_from_portfolio import get_asset_open_positions

from ..portfolio import Portfolio
from .utils import create_date_series_from_intervals, get_ticker_holding_intervals


@dataclass
class PortfolioTimeSeries(Portfolio):
    """
    DataFrame with the following structure:

    Columns:
    - Date (str): Date of the transaction or calculation.
    - Ticker (str): Asset symbol (including synthetic cash tickers like __EUR).
    - Quantity (int): Accumulated quantity of shares/units on the date.
    - Price (float): Share price on the date in original currency (1.0 for cash tickers).
    - Price_Base (float): Share price converted to portfolio base currency, including fees for purchase transactions.
    - Value (float): Total value of the shares/units on the date (Quantity * Price).
    - Value_Base (float): Total value in portfolio base currency (Quantity * Price_Base).
    - Cost (float): Total accumulated cost of the shares/units on the date in base currency.
    - Sector (str): Sector to which the asset belongs (Cash for synthetic tickers).
    - Country (str): Country to which the asset belongs.

    Each row represents the state of an asset on a specific date.
    Cash transactions use synthetic tickers (e.g., __EUR) with constant price of 1.0.
    """

    portfolio_timeseries: pd.DataFrame = field(init=False)

    def __post_init__(self):
        # super().__post_init__()
        self.portfolio_timeseries = self._build_portfolio_timeseries()

    def _build_portfolio_timeseries(self) -> pd.DataFrame:
        """
        Preprocesses portfolio data to generate a structured DataFrame, including cost calculation.

        Args:
            assets (list): List of assets with their transactions.
            start_date (datetime): Portfolio start date.
            data_provider (DataProvider): Data provider to obtain historical prices.

        Returns:
            pd.DataFrame: Structured DataFrame with the portfolio evolution.
        """

        records = []

        for ticker_asset in self.assets:
            dates = []
            historical_prices = []
            ticker = ticker_asset.ticker
            if ticker.startswith("__"):
                dates = pd.date_range(
                    start=self.start_date, end=pd.Timestamp.now(), freq="D"
                )
                historical_prices = pd.Series(1.0, index=dates)
            else:
                interval = get_ticker_holding_intervals(self.assets, ticker)
                dates = create_date_series_from_intervals(interval)
                historical_prices = self.data_provider.get_price_series_converted(
                    ticker, self.currency
                )

            latest_price = 0
            for date in dates:
                current_quantity = 0
                current_cost = 0

                # Calculate cost using the modularized function
                date_string = date.strftime("%Y-%m-%d")
                cost_info = get_asset_open_positions(ticker_asset, date_string)
                current_quantity = cost_info.quantity
                current_cost = cost_info.cost

                # cost_info = calculate_cost(date, ticker_asset.transactions)

                # current_quantity = cost_info["quantity"]
                # current_cost = cost_info["total_cost"]

                if date in historical_prices.index:
                    price = historical_prices.loc[date].item()
                    latest_price = price
                else:
                    price = latest_price

                value = current_quantity * price

                records.append(
                    {
                        "Date": date,
                        "Ticker": ticker,
                        "Quantity": current_quantity,
                        "Price": 0,
                        "Price_Base": price,
                        "Value": 0,
                        "Value_Base": value,
                        "Cost": current_cost,
                        "Sector": ticker_asset.sector,
                        "Country": ticker_asset.country,
                    }
                )

        # Convert records to DataFrame
        return pd.DataFrame(records)

    @classmethod
    def from_portfolio(cls, portfolio: "Portfolio") -> "PortfolioTimeSeries":
        """
        Alternate constructor that builds PortfolioTimeSeries from a Portfolio.
        """
        return PortfolioTimeSeries(
            name=portfolio.name,
            currency=portfolio.currency,
            assets=portfolio.assets,
            data_provider=portfolio.data_provider,
            account=portfolio.account,
            start_date=portfolio.start_date,
        )

    def print(self) -> None:
        from .print_date_frame import print_data_frame

        print_data_frame(self)

    def plot_evolution(self) -> LineChartData:
        from .plot_evolution import plot_portfolio_evolution

        return plot_portfolio_evolution(self)
