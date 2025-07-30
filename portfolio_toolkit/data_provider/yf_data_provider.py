import os
from datetime import datetime

import pandas as pd
import yfinance as yf

from .data_provider import DataProvider


class YFDataProvider(DataProvider):
    """
    Market data provider using Yahoo Finance.
    """

    # === Index tickers ===
    NASDAQ = "^IXIC"
    SP500 = "^GSPC"
    DOW_JONES = "^DJI"
    MERVAL = "^MERV"
    VIX = "^VIX"
    BONO_10_ANIOS_USA = "^TNX"
    DOLAR_INDEX = "DX-Y.NYB"

    # === Commodities tickers ===
    BRENT = "BZ=F"
    WTI = "CL=F"
    ORO = "GC=F"

    # === Currency tickers ===
    USDARS = "USDARS=X"
    USDEUR = "USDEUR=X"
    EURUSD = "EURUSD=X"

    # === Example stocks ===
    AAPL = "AAPL"
    MSFT = "MSFT"
    GOOGL = "GOOGL"
    AMZN = "AMZN"
    TSLA = "TSLA"
    META = "META"
    NVDA = "NVDA"
    INTC = "INTC"
    BA = "BA"
    YPF = "YPF"
    BBAR = "BBAR"
    BMA = "BMA"
    VALE = "VALE"
    ARCH = "ARCH"
    SLDP = "SLDP"
    LILMF = "LILMF"
    JOBY = "JOBY"
    NFE = "NFE"
    KOS = "KOS"
    BBD = "BBD"
    EVTL = "EVTL"

    def __init__(self):
        """
        Initializes the YFDataProvider class with in-memory caches for ticker data, info, and currencies.
        """
        self.cache = {}
        self.info_cache = {}
        self.currency_cache = {}

    def __load_ticker(self, ticker, periodo="5y", auto_adjust=False):
        """
        Private method to load ticker data into the cache. If the file exists, it loads it;
        otherwise, it downloads the data and saves it to a file.

        Args:
            ticker (str): The ticker symbol.
            periodo (str): The time period for historical data (default "5y").
            auto_adjust (bool): Whether to automatically adjust prices for splits/dividends (default True).

        Returns:
            pd.DataFrame: The historical data for the ticker.
        """
        cache_dir = "/tmp/portfolio_tools_cache"
        os.makedirs(cache_dir, exist_ok=True)
        archivo_existente = f"{cache_dir}/{datetime.now().strftime('%Y%m%d-%H')}-{ticker}-{periodo}_historical_data.pkl"

        if ticker in self.cache:
            # print(f"Using cached data for {ticker}")
            return self.cache[ticker]

        if os.path.exists(archivo_existente):
            # print(f"Loading data from local binary file: {archivo_existente}")
            datos = pd.read_pickle(archivo_existente)
        else:
            # print(f"Downloading data for {ticker}")
            datos = yf.download(
                ticker, period=periodo, auto_adjust=False, progress=False
            )
            datos.to_pickle(archivo_existente)
            # print(f"Data saved as binary in '{archivo_existente}'")

        self.cache[ticker] = datos
        return datos

    def __load_ticker_info(self, ticker):
        """
        Private method to load ticker info into the cache. If the file exists, it loads it;
        otherwise, it downloads the info and saves it to a file.

        Args:
            ticker (str): The ticker symbol.

        Returns:
            dict: The ticker information.
        """
        cache_dir = "/tmp/portfolio_tools_cache"
        os.makedirs(cache_dir, exist_ok=True)
        archivo_existente = (
            f"{cache_dir}/{datetime.now().strftime('%Y%m%d')}-{ticker}_info.pkl"
        )

        if ticker in self.info_cache:
            # print(f"Using cached info for {ticker}")
            return self.info_cache[ticker]

        if os.path.exists(archivo_existente):
            # print(f"Loading info from local binary file: {archivo_existente}")
            info = pd.read_pickle(archivo_existente)
        else:
            # print(f"Downloading info for {ticker}")
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info
            pd.to_pickle(info, archivo_existente)
            # print(f"Info saved as binary in '{archivo_existente}'")

        self.info_cache[ticker] = info
        return info

    def __load_ticker_currency(self, ticker):
        """
        Private method to load and cache ticker currency to avoid repeated calculations.

        Args:
            ticker (str): The ticker symbol.

        Returns:
            str: The currency code (e.g., 'USD', 'EUR', 'CAD').
        """
        if ticker in self.currency_cache:
            return self.currency_cache[ticker]

        # Special cases for known tickers
        currency_map = {
            # European stocks
            "ASML": "EUR",
            "SAP": "EUR",
            "ADYEN": "EUR",
            # Canadian stocks
            "SHOP": "CAD",
            "CNQ": "CAD",
            "TRI": "CAD",
            # UK stocks
            "SHEL": "GBP",
            "AZN": "GBP",
            "ULVR": "GBP",
            # Currency pairs
            "EURUSD=X": "USD",
            "GBPUSD=X": "USD",
            "USDCAD=X": "USD",
            "USDARS=X": "USD",
            # Commodities (typically USD)
            "GC=F": "USD",  # Gold
            "CL=F": "USD",  # Oil
            "BZ=F": "USD",  # Brent
        }

        # Check if ticker is in our special map
        if ticker in currency_map:
            currency = currency_map[ticker]
        else:
            try:
                info = self.get_ticker_info(ticker)
                # Try different possible currency fields in the info
                currency = (
                    info.get("currency")
                    or info.get("financialCurrency")
                    or info.get("tradeCurrency")
                )

                if currency:
                    currency = currency.upper()
                else:
                    # Default to USD if no currency information is found
                    currency = "USD"
            except Exception:
                # If there's any error getting info, default to USD
                currency = "USD"

        # Cache the result
        self.currency_cache[ticker] = currency
        return currency

    def __get_currency_pair_ticker(self, from_currency, to_currency):
        """
        Private method to get the Yahoo Finance ticker for a currency pair.

        Args:
            from_currency (str): Source currency code (e.g., 'USD').
            to_currency (str): Target currency code (e.g., 'EUR').

        Returns:
            str: Yahoo Finance currency pair ticker (e.g., 'USDEUR=X').
        """
        if from_currency == to_currency:
            return None

        # Common currency pairs in Yahoo Finance format
        currency_pairs = {
            ("USD", "EUR"): "USDEUR=X",
            ("EUR", "USD"): "EURUSD=X",
            ("USD", "CAD"): "USDCAD=X",
            ("CAD", "USD"): "CADUSD=X",
            ("USD", "GBP"): "USDGBP=X",
            ("GBP", "USD"): "GBPUSD=X",
            ("EUR", "CAD"): "EURCAD=X",
            ("CAD", "EUR"): "CADEUR=X",
            ("EUR", "GBP"): "EURGBP=X",
            ("GBP", "EUR"): "GBPEUR=X",
            ("CAD", "GBP"): "CADGBP=X",
            ("GBP", "CAD"): "GBPCAD=X",
        }

        pair = (from_currency, to_currency)
        if pair in currency_pairs:
            return currency_pairs[pair]

        # If not found, try the reverse pair
        reverse_pair = (to_currency, from_currency)
        if reverse_pair in currency_pairs:
            return currency_pairs[reverse_pair]

        # If still not found, construct the ticker (may not work for all pairs)
        return f"{from_currency}{to_currency}=X"

    def get_price(self, ticker, fecha):
        """
        Gets the price of an asset on a specific date.

        Args:
            ticker (str): The ticker symbol.
            fecha (datetime): The date for which to get the price.

        Returns:
            float: The asset price on the specified date.
        """
        datos = self.__load_ticker(ticker)
        if fecha in datos.index:
            return datos.loc[fecha, "Close"].item()  # Return closing price
        else:
            raise ValueError(f"No data available for ticker {ticker} on date {fecha}.")

    def get_raw_data(self, ticker, periodo="5y"):
        """
        Gets all historical data for a ticker directly.

        Args:
            ticker (str): The ticker symbol.
            periodo (str): The time period for historical data (default "5y").

        Returns:
            pd.DataFrame: The historical data for the ticker.

        Example DataFrame returned:

            #   Open    High     Low   Close  Adj Close   Volume
            #2024-07-01 10.00   10.50   9.80   10.20     10.10     1000000
            #2024-07-02 10.20   10.60  10.00   10.40     10.30     1200000
            #...         ...     ...     ...     ...       ...         ...
        """
        return self.__load_ticker(ticker, periodo)

    def get_price_series(self, ticker, columna="Close", period="5y"):
        """
        Gets the price series of an asset for a specific column.

        Args:
            ticker (str): The ticker symbol.
            columna (str): The price column to get (default "Close").

        Returns:
            pd.Series: Price series of the asset.
        """
        datos = self.__load_ticker(ticker, period)

        if columna in datos.columns:
            series = datos[columna]
            # Si es un DataFrame con una sola columna, convertir a Series
            if isinstance(series, pd.DataFrame):
                series = series.iloc[:, 0]
            return series
        else:
            raise ValueError(f"Column {columna} is not available for ticker {ticker}.")

    def get_ticker_info(self, ticker):
        """
        Gets detailed information for a ticker using yfinance's Ticker.info.

        Args:
            ticker (str): The ticker symbol.

        Returns:
            dict: Dictionary with company information and key statistics (e.g., P/E ratio, market cap, etc.).
        """
        return self.__load_ticker_info(ticker)

    def get_price_series_converted(self, ticker, target_currency, columna="Close"):
        """
        Gets the price series of an asset converted to a target currency.

        Args:
            ticker (str): The ticker symbol.
            target_currency (str): Target currency code (e.g., 'EUR', 'USD', 'CAD').
            columna (str): The price column to get (default "Close").

        Returns:
            pd.Series: Price series of the asset converted to target currency.
        """
        # Get original price series
        original_prices = self.get_price_series(ticker, columna)

        # Get the ticker's original currency
        original_currency = self.__load_ticker_currency(ticker)

        # If currencies are the same, return original prices
        if original_currency == target_currency:
            return original_prices

        # Get currency pair ticker
        currency_pair_ticker = self.__get_currency_pair_ticker(
            original_currency, target_currency
        )

        if currency_pair_ticker is None:
            raise ValueError(
                f"Cannot convert from {original_currency} to {target_currency}: same currency"
            )

        # Get exchange rate series
        try:
            exchange_rates = self.get_price_series(currency_pair_ticker, "Close")
        except Exception as e:
            raise ValueError(
                f"Cannot get exchange rates for {original_currency} to {target_currency}: {e}"
            )

        # Check if we need to invert the rates
        pair_to_from = self.__get_currency_pair_ticker(
            target_currency, original_currency
        )

        if currency_pair_ticker == pair_to_from:
            # We got the inverse pair, so we need to invert the rates
            exchange_rates = 1 / exchange_rates

        aligned_prices, aligned_rates = original_prices.align(
            exchange_rates, join="inner"
        )

        # Convert prices
        converted_prices = aligned_prices * aligned_rates

        # Set name to indicate conversion
        converted_prices.name = f"{ticker}_{columna}_{target_currency}"

        return converted_prices

    def get_ticker_currency(self, ticker):
        """
        Gets the currency of a ticker from its info.

        Args:
            ticker (str): The ticker symbol.

        Returns:
            str: The currency code (e.g., 'USD', 'EUR', 'CAD') or 'USD' as default.
        """
        return self.__load_ticker_currency(ticker)
