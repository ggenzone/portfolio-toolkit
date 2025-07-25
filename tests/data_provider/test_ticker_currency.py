import unittest
from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider


class TestTickerCurrency(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        self.data_provider = YFDataProvider()

    def test_us_stock_currency(self):
        """Test that US stocks return USD."""
        currency = self.data_provider.get_ticker_currency('AAPL')
        self.assertEqual(currency, 'USD')

    def test_canadian_stock_currency(self):
        """Test that Canadian stocks return CAD."""
        currency = self.data_provider.get_ticker_currency('DMX.V')
        self.assertEqual(currency, 'CAD')

    def test_european_stock_currency(self):
        """Test that European stocks return EUR."""
        currency = self.data_provider.get_ticker_currency('ASML.AS')
        self.assertEqual(currency, 'EUR')

    def test_currency_pair(self):
        """Test that currency pairs return base currency."""
        currency = self.data_provider.get_ticker_currency('EURUSD=X')
        self.assertEqual(currency, 'USD')

    def test_commodity_currency(self):
        """Test that commodities return USD."""
        currency = self.data_provider.get_ticker_currency('GC=F')
        self.assertEqual(currency, 'USD')

    def test_nonexistent_ticker(self):
        """Test that non-existent tickers default to USD."""
        currency = self.data_provider.get_ticker_currency('NONEXISTENT')
        self.assertEqual(currency, 'USD')

    def test_multiple_tickers(self):
        """Test multiple tickers at once."""
        expected_currencies = {
            'AAPL': 'USD',
            'DMX.V': 'CAD',
            'ASML.AS': 'EUR',
            'MSFT': 'USD',
        }
        
        for ticker, expected_currency in expected_currencies.items():
            with self.subTest(ticker=ticker):
                currency = self.data_provider.get_ticker_currency(ticker)
                self.assertEqual(currency, expected_currency)


if __name__ == '__main__':
    unittest.main()