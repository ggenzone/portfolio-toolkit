from typing import Optional

from portfolio_toolkit.data_provider.data_provider import DataProvider

from .portfolio_asset import PortfolioAsset


def create_portfolio_asset(
    data_provider: DataProvider, ticker: str, currency: Optional[str] = None
) -> PortfolioAsset:
    """
    Creates a PortfolioAsset object with market data using a data provider.

    Args:
        data_provider: The data provider instance to fetch ticker information and prices.
        ticker (str): The ticker for the asset.
        currency (Optional[str]): The currency for price data. If None, uses the asset's default currency.

    Returns:
        PortfolioAsset: The PortfolioAsset object with market data including:
                        - ticker
                        - sector
                        - prices (historical price data)
                        - info (ticker information from data provider)
                        - currency
                        - transactions (empty list)
    """
    # Get ticker information from data provider
    ticker_info = data_provider.get_ticker_info(ticker)

    # Determine currency - use provided currency or default from ticker info
    asset_currency = currency or data_provider.get_ticker_currency()

    # Get historical price data
    prices = data_provider.get_price_series_converted(
        ticker, target_currency=asset_currency
    )

    # Create and return a PortfolioAsset object
    return PortfolioAsset(
        ticker=ticker,
        prices=prices,
        info=ticker_info,
        currency=asset_currency,
        transactions=[],  # Initialize with an empty list of transactions
    )
