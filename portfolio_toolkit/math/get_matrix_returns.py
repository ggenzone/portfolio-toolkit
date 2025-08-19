from typing import List

import pandas as pd

from portfolio_toolkit.asset import MarketAsset
from portfolio_toolkit.math.get_log_returns import get_log_returns


def get_matrix_returns(market_assets: List[MarketAsset]) -> pd.DataFrame:
    """
    Creates a DataFrame of logarithmic returns from a list of MarketAsset objects.

    Args:
        market_assets (List[MarketAsset]): List of MarketAsset objects, each containing
                                         a 'price' attribute as pd.Series with price data

    Returns:
        pd.DataFrame: DataFrame where:
            - Rows are dates (datetime index from price series)
            - Columns are ticker symbols from MarketAsset.ticker
            - Values are logarithmic returns calculated using get_log_returns()

    Example:
        >>> market_assets = [
        ...     MarketAsset(ticker="AAPL", price=aapl_prices),
        ...     MarketAsset(ticker="MSFT", price=msft_prices),
        ...     MarketAsset(ticker="GOOGL", price=googl_prices)
        ... ]
        >>> returns_df = get_matrix_returns(market_assets)
        >>> print(returns_df.head())

                    AAPL      MSFT     GOOGL
        2023-01-01   NaN       NaN       NaN
        2023-01-02  0.0123   0.0089   0.0156
        2023-01-03 -0.0067   0.0034  -0.0023

    Notes:
        - First row will contain NaN values (no previous price for return calculation)
        - Uses get_log_returns() function for consistent logarithmic return calculation
        - Automatically aligns dates across all assets
        - Missing data points will appear as NaN in the resulting DataFrame
    """
    if not market_assets:
        raise ValueError("Market assets list cannot be empty")

    returns_data = {}

    # Calculate returns for each market asset
    for asset in market_assets:
        if not hasattr(asset, "ticker"):
            raise ValueError("MarketAsset must have 'ticker' attribute")

        if not hasattr(asset, "prices"):
            raise ValueError(f"MarketAsset {asset.ticker} must have 'prices' attribute")

        if not isinstance(asset.prices, pd.Series):
            raise ValueError(
                f"MarketAsset {asset.ticker} 'prices' must be a pandas Series"
            )

        if asset.prices.empty:
            raise ValueError(f"MarketAsset {asset.ticker} has empty prices series")

        # Calculate log returns for this asset
        log_returns = get_log_returns(asset.prices)
        returns_data[asset.ticker] = log_returns

    # Create DataFrame with dates as rows and tickers as columns
    returns_df = pd.DataFrame(returns_data)

    # Sort by date index to ensure chronological order
    returns_df = returns_df.sort_index()

    return returns_df


def get_matrix_returns_aligned(
    market_assets: List[MarketAsset], start_date: str = None, end_date: str = None
) -> pd.DataFrame:
    """
    Creates an aligned DataFrame of returns with optional date filtering.

    Args:
        market_assets: List of MarketAsset objects
        start_date: Start date in 'YYYY-MM-DD' format (optional)
        end_date: End date in 'YYYY-MM-DD' format (optional)

    Returns:
        pd.DataFrame: Aligned returns DataFrame with only overlapping dates

    Example:
        >>> # Get returns for specific period
        >>> returns_df = get_matrix_returns_aligned(
        ...     market_assets,
        ...     start_date="2023-01-01",
        ...     end_date="2023-12-31"
        ... )
    """
    # Get base returns matrix
    returns_df = get_matrix_returns(market_assets)

    # Filter by date range if specified
    if start_date:
        returns_df = returns_df[returns_df.index >= start_date]

    if end_date:
        returns_df = returns_df[returns_df.index <= end_date]

    # Drop rows where all values are NaN (no data for any asset)
    returns_df = returns_df.dropna(how="all")

    return returns_df
