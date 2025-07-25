import unittest
from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider

class TestYFDataProvider(unittest.TestCase):
    def setUp(self):
        self.provider = YFDataProvider()

    def test_get_raw_data(self):
        df = self.provider.get_raw_data('AAPL', periodo='1mo')
        self.assertFalse(df.empty)
        self.assertIn('Close', df.columns)

    def test_get_ticker_info(self):
        info = self.provider.get_ticker_info('AAPL')
        self.assertIsInstance(info, dict)
        self.assertIn('symbol', info)

if __name__ == '__main__':
    unittest.main()
