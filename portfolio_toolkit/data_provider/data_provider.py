from abc import ABC, abstractmethod


class DataProvider(ABC):
    """
    Common interface for market data providers.
    """

    @abstractmethod
    def get_price(self, ticker, date):
        """
        Gets the price of an asset on a specific date.

        Args:
            ticker (str): The ticker symbol.
            date (datetime): The date for which to get the price.

        Returns:
            float: The price of the asset on the specified date.
        """
        pass

    @abstractmethod
    def get_raw_data(self, ticker, period="5y"):
        """
        Gets all historical data for a ticker.

        Args:
            ticker (str): The ticker symbol.
            period (str): The time period for historical data (default "5y").

        Returns:
            pd.DataFrame: The historical data for the ticker.
        """
        pass

    @abstractmethod
    def get_price_series(self, ticker, column="Close"):
        """
        Gets the price series of an asset for a specific column.

        Args:
            ticker (str): The ticker symbol.
            column (str): The price column to get (default "Close").

        Returns:
            pd.Series: Price series of the asset.
        """
        pass

    @abstractmethod
    def get_price_series_converted(self, ticker, target_currency, column="Close"):
        """
        Gets the price series of an asset for a specific column, converted to a target currency.

        Args:
            ticker (str): The ticker symbol.
            target_currency (str): The currency to convert prices to.
            column (str): The price column to get (default "Close").

        Returns:
            pd.Series: Price series of the asset in the target currency.
        """
        pass

    @abstractmethod
    def get_ticker_info(self, ticker):
        """
        Gets detailed information for a ticker (e.g., P/E ratio, market cap, etc.).

        Args:
            ticker (str): The ticker symbol.

        Returns:
            dict: Dictionary with company information and key statistics.
        """
        pass
