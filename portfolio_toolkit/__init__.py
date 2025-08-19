"""Portfolio Toolkit - A comprehensive toolkit for portfolio analysis and management."""

__version__ = "0.2.0"
__author__ = "Guido Genzone"

# Main imports for easy access
try:
    from .data_provider.yf_data_provider import YFDataProvider
    from .portfolio import Portfolio
    from .watchlist import Watchlist
except ImportError:
    # Handle import errors gracefully during development
    pass

__all__ = [
    "__version__",
    "__author__",
    "Portfolio",
    "Watchlist",
    "YFDataProvider",
]
