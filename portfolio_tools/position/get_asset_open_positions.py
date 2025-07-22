from datetime import datetime

from portfolio_tools.asset.portfolio_asset import PortfolioAsset

from .valued_position import ValuedPosition


def get_asset_open_positions(asset: PortfolioAsset, date: str) -> ValuedPosition:
    """
    Computes the open position of an asset as of a given date.

    Args:
        asset (PortfolioAsset): The asset containing transactions.
        date (str): The date up to which the position is calculated (YYYY-MM-DD).

    Returns:
        ValuedPosition: An object representing the open position with valuation.
    """

    transactions = sorted(
        [tx for tx in asset.transactions if tx.date <= date],
        key=lambda x: x.date,
    )

    quantity = 0
    cost = 0

    for tx in transactions:
        if tx.transaction_type == "buy" or tx.transaction_type == "deposit":
            quantity += tx.quantity
            cost += tx.total_base
        elif tx.transaction_type == "sell" or tx.transaction_type == "withdrawal":
            quantity_to_deduct = min(quantity, tx.quantity)
            average_price = cost / quantity if quantity > 0 else 0
            cost -= quantity_to_deduct * average_price
            quantity -= quantity_to_deduct

    average_price = cost / quantity if quantity > 0 else 0

    # Calculate market value if asset has price data
    current_price = 0

    if quantity > 0 and asset.prices is not None:
        try:
            # Convert date string to datetime for price lookup
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
            prices_series = asset.prices

            # Find the closest available price date (on or before target date)
            available_dates = [
                d.date() for d in prices_series.index if d.date() <= target_date
            ]

            if available_dates:
                closest_date = max(available_dates)
                # Find the corresponding datetime index
                matching_datetime = None
                for dt in prices_series.index:
                    if dt.date() == closest_date:
                        matching_datetime = dt
                        break

                if matching_datetime is not None:
                    current_price = float(prices_series.loc[matching_datetime])
        except (ValueError, KeyError, IndexError, TypeError):
            # If there's any error getting the price, current_price remains 0
            pass

    # Create and return a ValuedPosition object
    return ValuedPosition(
        ticker=asset.ticker,
        sector=asset.sector,
        country=asset.country,
        buy_price=average_price,
        quantity=quantity,
        current_price=current_price,
    )
