from datetime import datetime

import pandas as pd

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


def preprocess_data(assets, start_date, data_provider):
    """
    Preprocesses portfolio data to generate a structured DataFrame, including cost calculation.

    Args:
        assets (list): List of assets with their transactions.
        start_date (datetime): Portfolio start date.
        data_provider (DataProvider): Data provider to obtain historical prices.

    Returns:
        pd.DataFrame: Structured DataFrame with the portfolio evolution.
    """
    historical_prices = {}
    for asset in assets:
        ticker = asset["ticker"]
        if ticker not in historical_prices:
            # For cash tickers (starting with __), use a constant price of 1
            if ticker.startswith("__"):
                # Create a price series with value 1 for all dates from start_date onwards
                date_range = pd.date_range(
                    start=start_date, end=pd.Timestamp.now(), freq="D"
                )
                historical_prices[ticker] = pd.Series(1.0, index=date_range)
            else:
                # For real assets, get historical prices from data provider
                historical_prices[ticker] = data_provider.get_price_series(ticker)

    records = []

    for ticker, prices in historical_prices.items():
        dates = prices.index
        dates = [
            date for date in dates if date >= start_date
        ]  # Filter dates from start_date

        for date in dates:
            ticker_asset = None  # Initialize the asset for the ticker
            for asset in assets:
                if asset["ticker"] == ticker:
                    ticker_asset = asset
                    break

            current_quantity = 0
            current_cost = 0

            # Calculate cost using the modularized function
            cost_info = calculate_cost(date, ticker_asset["transactions"])

            current_quantity = cost_info["quantity"]
            current_cost = cost_info["total_cost"]

            price = prices.loc[date].item()
            value = current_quantity * price

            # Calculate price in base currency with fees absorbed
            price_base = get_price_base_with_fees(ticker, date, price, assets)

            # Calculate current market value in base currency (for display purposes)
            current_market_value_base = convert_price_to_base_currency(
                ticker, price, assets
            )
            value_base = current_quantity * current_market_value_base

            records.append(
                {
                    "Date": date,
                    "Ticker": ticker,
                    "Quantity": current_quantity,
                    "Price": price,
                    "Price_Base": price_base,
                    "Value": value,
                    "Value_Base": value_base,
                    "Cost": current_cost,
                    "Sector": ticker_asset["sector"],
                    "Country": ticker_asset["country"],
                }
            )

    result_df = pd.DataFrame(records)
    # result_df['Date'] = result_df['Date'].astype(str)  # Convert Timestamp to string
    # # Save the data to output.json for debugging
    # with open('output.json', 'w') as file:
    #   json.dump(result_df.to_dict(orient='records'), file, indent=4)

    return result_df


def convert_price_to_base_currency(ticker, market_price, assets):
    """
    Converts a current market price to the portfolio's base currency using
    the most recent exchange rate from transactions.

    Args:
        ticker (str): Asset ticker symbol.
        market_price (float): Current market price in asset's currency.
        assets (list): List of assets with transactions.

    Returns:
        float: Market price converted to base currency.
    """
    # For cash tickers, always return 1.0
    if ticker.startswith("__"):
        return 1.0

    # Find the asset and get the most recent exchange rate
    ticker_asset = None
    for asset in assets:
        if asset["ticker"] == ticker:
            ticker_asset = asset
            break

    if not ticker_asset or not ticker_asset["transactions"]:
        return market_price  # Fallback to original price

    # Get the most recent exchange rate from transactions
    most_recent_rate = 1.0
    for transaction in reversed(ticker_asset["transactions"]):  # Start from most recent
        if "exchange_rate" in transaction:
            most_recent_rate = transaction["exchange_rate"]
            break

    # Convert market price to base currency
    return market_price / most_recent_rate


def get_price_base_with_fees(ticker, date, original_price, assets):
    """
    Calculates the effective price in base currency for a ticker on a specific date,
    including fees absorbed into the price for purchase transactions.

    Args:
        ticker (str): Asset ticker symbol.
        date (datetime): Date for price calculation.
        original_price (float): Original market price in asset's currency.
        assets (list): List of assets with transactions.

    Returns:
        float: Price in base currency including fees for purchase transactions.
    """
    # For cash tickers, always return 1.0
    if ticker.startswith("__"):
        return 1.0

    # Find the asset
    ticker_asset = None
    for asset in assets:
        if asset["ticker"] == ticker:
            ticker_asset = asset
            break

    if not ticker_asset:
        return original_price  # Fallback to original price

    # Calculate total cost and quantity up to this date to get effective price
    cost_info = calculate_cost(date, ticker_asset["transactions"])

    if cost_info["quantity"] > 0:
        # Use the average cost per unit which includes fees and exchange rate
        return cost_info["average_price"]
    else:
        # No transactions yet, return original price
        return original_price


def calculate_cost(date, transactions):
    """
    Calculates the accumulated quantity, average price, and total cost of shares/units
    up to a specific date using FIFO method. Handles both asset transactions (buy/sell)
    and cash transactions (deposit/withdrawal).

    Uses total_base for cost calculation, which includes fees and is converted to
    the portfolio's base currency (EUR).

    Args:
        date (datetime): Cutoff date to calculate the values.
        transactions (list): List of transactions with format including total_base field.
                           Supported types: "buy", "sell", "deposit", "withdrawal".

    Returns:
        dict: Dictionary with accumulated quantity, average price, and total cost in base currency.
    """
    current_quantity = 0
    total_cost = 0
    fifo = (
        []
    )  # List to handle purchases (FIFO): (quantity, cost_per_unit_in_base_currency)

    for transaction in transactions:
        transaction_date = datetime.strptime(transaction["date"], "%Y-%m-%d")
        if transaction_date <= date:
            if transaction["type"] == "buy" or transaction["type"] == "deposit":
                # Use total_base which includes fees and is in base currency (EUR)
                total_cost_base = transaction.get(
                    "total_base", transaction["quantity"] * transaction["price"]
                )
                cost_per_unit = (
                    total_cost_base / transaction["quantity"]
                    if transaction["quantity"] > 0
                    else 0
                )

                # Update FIFO and total cost
                fifo.append((transaction["quantity"], cost_per_unit))
                current_quantity += transaction["quantity"]
                total_cost += total_cost_base

            elif transaction["type"] == "sell" or transaction["type"] == "withdrawal":
                # Update FIFO and cost according to shares sold (FIFO method)
                quantity_sold = transaction["quantity"]
                current_quantity -= quantity_sold

                while quantity_sold > 0 and fifo:
                    fifo_quantity, fifo_cost_per_unit = fifo[0]
                    if fifo_quantity <= quantity_sold:
                        # Sell the entire FIFO lot
                        quantity_sold -= fifo_quantity
                        total_cost -= fifo_quantity * fifo_cost_per_unit
                        fifo.pop(0)
                    else:
                        # Sell part of the FIFO lot
                        fifo[0] = (fifo_quantity - quantity_sold, fifo_cost_per_unit)
                        total_cost -= quantity_sold * fifo_cost_per_unit
                        quantity_sold = 0

    # Calculate average price in base currency
    average_price = total_cost / current_quantity if current_quantity > 0 else 0

    return {
        "quantity": current_quantity,
        "average_price": average_price,
        "total_cost": total_cost,
    }
