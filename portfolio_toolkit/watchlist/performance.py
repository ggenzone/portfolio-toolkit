from typing import List

import pandas as pd

from portfolio_toolkit.asset import MarketAsset
from portfolio_toolkit.utils.period import Period


def performance(assets: List[MarketAsset], periods: List[Period]) -> pd.DataFrame:
    """
    Calculate performance comparison between periods for each asset.

    Parameters:
    -----------
    assets : List[MarketAsset]
        List of market assets with price data
    periods : List[Period]
        List of periods to compare

    Returns:
    --------
    pd.DataFrame
        DataFrame where rows are assets (tickers) and columns are period labels.
        Each cell contains the percentage change from previous period to current period.
        First period column will contain '-' as there's no previous period to compare.
    """
    # Get all asset tickers
    all_assets = {asset.ticker for asset in assets}

    # Create mapping from ticker to asset for easy lookup
    asset_map = {asset.ticker: asset for asset in assets}

    # Get prices for each period end date
    period_prices = {}

    for period in periods:
        end_date_str = period.end_date.strftime("%Y-%m-%d")
        period_prices[period.label] = {}

        for ticker in all_assets:
            asset = asset_map[ticker]
            # Get price at period end date (or closest available date)
            if hasattr(asset, "prices") and asset.prices is not None:
                # Find the closest date to period end date
                available_dates = asset.prices.index
                # Filter dates up to the period end date
                valid_dates = available_dates[available_dates <= end_date_str]

                if len(valid_dates) > 0:
                    # Get the latest available price before or at period end
                    closest_date = valid_dates.max()
                    period_prices[period.label][ticker] = asset.prices.loc[closest_date]
                else:
                    # No price data available for this period
                    period_prices[period.label][ticker] = None
            else:
                period_prices[period.label][ticker] = None

    # Create comparison data (percentage changes)
    comparison_data = {}
    period_labels = [period.label for period in periods]

    for ticker in sorted(all_assets):
        comparison_data[ticker] = []

        for i, period_label in enumerate(period_labels):
            if i == 0:
                continue
                # First period has no comparison
                # comparison_data[ticker].append('-')
            else:
                # Calculate percentage change from previous period
                current_price = period_prices[period_label][ticker]
                previous_price = period_prices[period_labels[i - 1]][ticker]

                if (
                    current_price is not None
                    and previous_price is not None
                    and previous_price != 0
                ):
                    # Calculate percentage change: (current - previous) / previous * 100
                    pct_change = (
                        (current_price - previous_price) / previous_price
                    ) * 100
                    comparison_data[ticker].append(f"{pct_change:.2f}%")
                else:
                    # Missing data or division by zero
                    comparison_data[ticker].append("-")

    period_labels = period_labels[1:]  # Skip first label as it has no comparison

    # Create DataFrame
    df = pd.DataFrame(comparison_data, index=period_labels).T

    return df
