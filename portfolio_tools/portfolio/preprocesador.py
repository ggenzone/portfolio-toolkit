from typing import List

import pandas as pd

from portfolio_tools.asset.portfolio_asset import PortfolioAsset
from portfolio_tools.data_provider.data_provider import DataProvider
from portfolio_tools.portfolio.utils import (
    create_date_series_from_intervals,
    get_ticker_holding_intervals,
)
from portfolio_tools.position.get_asset_open_positions import get_asset_open_positions

"""
The function `preprocess_data` returns a DataFrame with the following structure:

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


def preprocess_data(
    assets: List[PortfolioAsset],
    start_date: str,
    data_provider: DataProvider,
    currency="EUR",
):
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

    for ticker_asset in assets:
        dates = []
        historical_prices = []
        ticker = ticker_asset.ticker
        if ticker.startswith("__"):
            dates = pd.date_range(start=start_date, end=pd.Timestamp.now(), freq="D")
            historical_prices = pd.Series(1.0, index=dates)
        else:
            interval = get_ticker_holding_intervals(assets, ticker)
            dates = create_date_series_from_intervals(interval)
            historical_prices = data_provider.get_price_series_converted(
                ticker, currency
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

    result_df = pd.DataFrame(records)
    # result_df['Date'] = result_df['Date'].astype(str)  # Convert Timestamp to string
    # # Save the data to output.json for debugging
    # with open('output.json', 'w') as file:
    #   json.dump(result_df.to_dict(orient='records'), file, indent=4)

    return result_df
