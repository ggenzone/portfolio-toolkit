"""Portfolio Toolkit - A comprehensive toolkit for portfolio analysis and management."""

__version__ = "0.1.0"
__author__ = "Guido Genzone"

# Main imports for easy access
try:
    from .asset.portfolio_asset import PortfolioAsset
    from .data_provider.yf_data_provider import YFDataProvider
    from .portfolio.portfolio import Portfolio
except ImportError:
    # Handle import errors gracefully during development
    pass

__all__ = [
    "__version__",
    "__author__",
    "Portfolio",
    "PortfolioAsset",
    "YFDataProvider",
]
