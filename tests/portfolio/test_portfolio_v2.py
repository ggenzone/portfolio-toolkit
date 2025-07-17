import unittest
import os
from datetime import datetime
from portfolio_tools.portfolio.parser import load_json
from portfolio_tools.portfolio.portfolio import Portfolio
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider

class TestPortfolioV2(unittest.TestCase):
    def setUp(self):
        """Set up test data using external JSON files"""
        self.data_provider = YFDataProvider()
        self.examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
        self.test_json_path = os.path.join(self.examples_dir, 'test_portfolio_v2.json')
        self.basic_portfolio_path = os.path.join(self.examples_dir, 'basic_portfolio.json')
        self.multi_currency_path = os.path.join(self.examples_dir, 'multi_currency_portfolio.json')
        self.fifo_test_path = os.path.join(self.examples_dir, 'fifo_test_portfolio.json')
        self.cash_only_path = os.path.join(self.examples_dir, 'cash_only_portfolio.json')

    def test_load_json_parser(self):
        """Test the load_json parser function"""
        portfolio, start_date = load_json(self.test_json_path)
        
        # Test portfolio structure
        self.assertEqual(portfolio["name"], "Test Portfolio")
        self.assertEqual(portfolio["currency"], "EUR")
        self.assertIn("assets", portfolio)
        
        # Test start date
        self.assertEqual(start_date, datetime(2025, 6, 10))
        
        # Test assets grouping
        assets = portfolio["assets"]
        self.assertEqual(len(assets), 2)  # AAPL and __EUR

    def test_portfolio_class_initialization(self):
        """Test Portfolio class initialization with v2 format"""
        portfolio = Portfolio(self.test_json_path, self.data_provider)
        
        # Test portfolio properties
        self.assertEqual(portfolio.name, "Test Portfolio")
        self.assertEqual(portfolio.currency, "EUR")
        self.assertEqual(len(portfolio.assets), 2)
        self.assertIsNotNone(portfolio.start_date)

    def test_portfolio_helper_methods(self):
        """Test Portfolio helper methods"""
        portfolio = Portfolio(self.test_json_path, self.data_provider)
        
        # Test get_cash_transactions - now includes synthetic transactions
        cash_transactions = portfolio.get_cash_transactions()
        self.assertGreaterEqual(len(cash_transactions), 2)  # At least 2 original + synthetic ones
        
        # Find original cash transactions (deposit/withdrawal)
        original_cash = [t for t in cash_transactions if t["type"] in ["deposit", "withdrawal"]]
        self.assertEqual(len(original_cash), 2)
        self.assertEqual(original_cash[0]["type"], "deposit")
        self.assertEqual(original_cash[1]["type"], "withdrawal")
        
        # Test get_stock_assets
        stock_assets = portfolio.get_stock_assets()
        self.assertEqual(len(stock_assets), 1)
        self.assertEqual(stock_assets[0]["ticker"], "AAPL")
        
        # Test is_cash_ticker
        self.assertTrue(portfolio.is_cash_ticker("__EUR"))
        self.assertFalse(portfolio.is_cash_ticker("AAPL"))

    def test_calculate_current_quantity_stocks(self):
        """Test quantity calculation for stocks"""
        portfolio = Portfolio(self.test_json_path, self.data_provider)
        
        # After buy (10 shares)
        quantity_after_buy = portfolio.calculate_current_quantity("AAPL", datetime(2025, 6, 12))
        self.assertEqual(quantity_after_buy, 10)
        
        # After sell (5 shares remaining)
        quantity_after_sell = portfolio.calculate_current_quantity("AAPL", datetime(2025, 6, 13))
        self.assertEqual(quantity_after_sell, 5)

    def test_calculate_current_quantity_cash(self):
        """Test quantity calculation for cash transactions"""
        portfolio = Portfolio(self.test_json_path, self.data_provider)
        
        # After deposit (3000.00 EUR, not 1 unit)
        cash_after_deposit = portfolio.calculate_current_quantity("__EUR", datetime(2025, 6, 10))
        self.assertEqual(cash_after_deposit, 3000.0)
        
        # After all transactions (should reflect final cash balance)
        cash_after_all = portfolio.calculate_current_quantity("__EUR", datetime(2025, 6, 15))
        # This will depend on synthetic transactions from stock trades
        self.assertIsInstance(cash_after_all, (int, float))  # Just verify it's a number

    def test_basic_portfolio(self):
        """Test basic portfolio with simple transactions"""
        portfolio = Portfolio(self.basic_portfolio_path, self.data_provider)
        
        self.assertEqual(portfolio.name, "Basic Portfolio Test")
        self.assertEqual(portfolio.currency, "EUR")
        self.assertEqual(len(portfolio.assets), 2)  # __EUR and AAPL

    def test_multi_currency_portfolio(self):
        """Test portfolio with multiple currencies"""
        portfolio = Portfolio(self.multi_currency_path, self.data_provider)
        
        self.assertEqual(portfolio.name, "Multi Currency Portfolio Test")
        self.assertEqual(portfolio.currency, "EUR")
        # Should have __EUR, AAPL, and SHOP
        asset_tickers = [asset["ticker"] for asset in portfolio.assets]
        self.assertIn("__EUR", asset_tickers)
        self.assertIn("AAPL", asset_tickers)
        self.assertIn("SHOP", asset_tickers)

    def test_fifo_calculation(self):
        """Test FIFO calculation with multiple buys and sells"""
        portfolio = Portfolio(self.fifo_test_path, self.data_provider)
        
        # After buying 10 + 5 = 15 shares, then selling 8, should have 7 shares
        final_quantity = portfolio.calculate_current_quantity("AAPL", datetime(2025, 6, 14))
        self.assertEqual(final_quantity, 7)

    def test_cash_only_portfolio(self):
        """Test portfolio with only cash transactions"""
        portfolio = Portfolio(self.cash_only_path, self.data_provider)
        
        self.assertEqual(portfolio.name, "Cash Only Portfolio Test")
        self.assertEqual(len(portfolio.assets), 1)  # Only __EUR
        
        # Should have 1000 + 500 - 200 = 1300 EUR (fees don't reduce quantity)
        final_quantity = portfolio.calculate_current_quantity("__EUR", datetime(2025, 6, 20))
        self.assertEqual(final_quantity, 1300.0)

if __name__ == '__main__':
    unittest.main()