import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import numpy as np
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
        Initializes the YFDataProvider class with an in-memory cache for ticker data.
        """
        self.cache = {}

    def __load_ticker(self, ticker, periodo="5y"):
        """
        Private method to load ticker data into the cache. If the file exists, it loads it;
        otherwise, it downloads the data and saves it to a file.

        Args:
            ticker (str): The ticker symbol.
            periodo (str): The time period for historical data (default "5y").

        Returns:
            pd.DataFrame: The historical data for the ticker.
        """
        archivo_existente = f"temp/{datetime.now().strftime('%Y%m%d')}-{ticker}_historical_data.pkl"

        # Ensure temp directory exists
        os.makedirs("temp", exist_ok=True)

        if ticker in self.cache:
            # print(f"Using cached data for {ticker}")
            return self.cache[ticker]

        if os.path.exists(archivo_existente):
            # print(f"Loading data from local binary file: {archivo_existente}")
            datos = pd.read_pickle(archivo_existente)
        else:
            # print(f"Downloading data for {ticker}")
            datos = yf.download(ticker, period=periodo)
            datos.to_pickle(archivo_existente)
            # print(f"Data saved as binary in '{archivo_existente}'")

        self.cache[ticker] = datos
        return datos

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
            return datos.loc[fecha, 'Close'].item()  # Return closing price
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

    def get_price_series(self, ticker, columna="Close"):
        """
        Gets the price series of an asset for a specific column.

        Args:
            ticker (str): The ticker symbol.
            columna (str): The price column to get (default "Close").

        Returns:
            pd.Series: Price series of the asset.
        """
        datos = self.__load_ticker(ticker)
        if columna in datos.columns:
            return datos[columna]
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
        ticker_obj = yf.Ticker(ticker)
        return ticker_obj.info


