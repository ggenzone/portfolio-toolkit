from datetime import datetime
import pandas as pd
import json

"""
The function `preprocess_data` returns a DataFrame with the following structure:

Columns:
- Date (str): Date of the transaction or calculation.
- Ticker (str): Asset symbol.
- Quantity (int): Accumulated quantity of shares on the date.
- Price (float): Share price on the date.
- Value (float): Total value of the shares on the date (Quantity * Price).
- Cost (float): Total accumulated cost of the shares on the date.
- Sector (str): Sector to which the asset belongs.
- Country (str): Country to which the asset belongs.

Each row represents the state of an asset on a specific date.
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
        if asset["ticker"] not in historical_prices:
            historical_prices[asset["ticker"]] = data_provider.get_price_series(asset["ticker"])

    records = []

    for ticker, prices in historical_prices.items():
        dates = prices.index
        dates = [date for date in dates if date >= start_date]  # Filter dates from start_date

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

            records.append({
                "Date": date,
                "Ticker": ticker,
                "Quantity": current_quantity,
                "Price": price,
                "Value": value,
                "Cost": current_cost,
                "Sector": ticker_asset["sector"],
                "Country": ticker_asset["country"]
            })

    result_df = pd.DataFrame(records)
    # result_df['Date'] = result_df['Date'].astype(str)  # Convert Timestamp to string
    # # Save the data to output.json for debugging
    # with open('output.json', 'w') as file:
    #   json.dump(result_df.to_dict(orient='records'), file, indent=4)

    return result_df


def calculate_cost(date, transactions):
    """
    Calculates the accumulated quantity, average price, and total cost of shares
    up to a specific date.

    Args:
        date (datetime): Cutoff date to calculate the values.
        transactions (list): List of transactions with format [{"date": str, "type": str, "quantity": int, "price": float}].

    Returns:
        dict: Dictionary with accumulated quantity, average price, and total cost.
    """
    current_quantity = 0
    total_cost = 0
    fifo = [] # List to handle purchases (FIFO)

    for transaction in transactions:
        transaction_date = datetime.strptime(transaction["date"], "%Y-%m-%d")
        if transaction_date <= date:
            if transaction["type"] == "buy":
                # Update FIFO and total cost
                fifo.append((transaction["quantity"], transaction["price"]))
                current_quantity += transaction["quantity"]
                total_cost += transaction["quantity"] * transaction["price"]
            elif transaction["type"] == "sell":
                # Update FIFO and cost according to shares sold
                quantity_sold = transaction["quantity"]
                current_quantity -= quantity_sold
                while quantity_sold > 0 and fifo:
                    fifo_quantity, fifo_price = fifo[0]
                    if fifo_quantity <= quantity_sold:
                        # Sell the entire FIFO lot
                        quantity_sold -= fifo_quantity
                        total_cost -= fifo_quantity * fifo_price
                        fifo.pop(0)
                    else:
                        # Sell part of the FIFO lot
                        fifo[0] = (fifo_quantity - quantity_sold, fifo_price)
                        total_cost -= quantity_sold * fifo_price
                        quantity_sold = 0

    # Calculate average price
    average_price = total_cost / current_quantity if current_quantity > 0 else 0

    return {
        "quantity": current_quantity,
        "average_price": average_price,
        "total_cost": total_cost
    }