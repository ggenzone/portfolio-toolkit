import pandas as pd


def get_ticker_holding_intervals(assets, ticker):  # noqa: C901
    """
    Returns the date intervals where a specific ticker was held in the portfolio.

    Args:
        ticker (str): The ticker symbol to analyze.

    Returns:
        list: List of tuples with (start_date, end_date) intervals where the ticker was held.
              Returns empty list if ticker was never held or is not found.

    Example:
        [('2025-06-01', '2025-06-10'), ('2025-06-20', '2025-07-03')]
    """
    # Find the asset with the given ticker
    asset_transactions = None
    for asset in assets:
        if asset.ticker == ticker:
            asset_transactions = asset.transactions
            break

    if not asset_transactions:
        return []

    # Sort transactions by date
    sorted_transactions = sorted(asset_transactions, key=lambda x: x.date)

    intervals = []
    current_quantity = 0
    holding_start = None

    for transaction in sorted_transactions:
        date = transaction.date
        transaction_type = transaction.transaction_type
        quantity = transaction.quantity

        # Calculate new quantity after transaction
        if transaction_type == "buy":
            new_quantity = current_quantity + quantity
        elif transaction_type == "sell":
            new_quantity = current_quantity - quantity
        else:
            continue  # Skip other transaction types

        # Check if we're starting to hold
        if current_quantity == 0 and new_quantity > 0:
            holding_start = date

        # Check if we stopped holding
        elif current_quantity > 0 and new_quantity == 0:
            if holding_start:
                intervals.append((holding_start, date))
                holding_start = None

        current_quantity = new_quantity

    # If we're still holding at the end, add interval until today
    if current_quantity > 0 and holding_start:
        from datetime import datetime

        today = datetime.now().strftime("%Y-%m-%d")
        intervals.append((holding_start, today))

    return intervals


def create_date_series_from_intervals(intervals):
    """
    Creates a pandas Series with all dates from multiple intervals.

    Args:
        intervals (list): List of tuples with (start_date, end_date)

    Returns:
        pd.DatetimeIndex: Series with all dates from the intervals
    """
    all_dates = []

    for start_date, end_date in intervals:
        date_range = pd.date_range(start=start_date, end=end_date, freq="D")
        all_dates.extend(date_range)

    # Remove duplicates and sort
    unique_dates = pd.DatetimeIndex(sorted(set(all_dates)))
    return unique_dates
