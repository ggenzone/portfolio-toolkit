import unittest
import pandas as pd
import numpy as np
from portfolio_toolkit.utils.log_returns import calculate_log_returns


class TestLogReturns(unittest.TestCase):
    """Test suite for the calculate_log_returns function."""

    def test_calculate_log_returns(self):
        """Test the calculation of logarithmic returns."""
        # Create a sample price series
        prices = pd.Series([100, 105, 110, 120, 115])

        # Expected log returns
        expected_returns = prices.pct_change().apply(lambda x: np.log(1 + x))

        # Calculate log returns using the function
        calculated_returns = calculate_log_returns(prices)

        # Assert that the calculated returns match the expected returns
        pd.testing.assert_series_equal(calculated_returns, expected_returns, check_dtype=False)

    def test_empty_series(self):
        """Test the function with an empty series."""
        prices = pd.Series(dtype=float)
        expected_returns = pd.Series(dtype=float)
        calculated_returns = calculate_log_returns(prices)
        pd.testing.assert_series_equal(calculated_returns, expected_returns, check_dtype=False)

    def test_single_value_series(self):
        """Test the function with a single value series."""
        prices = pd.Series([100])
        expected_returns = pd.Series([np.nan])
        calculated_returns = calculate_log_returns(prices)
        pd.testing.assert_series_equal(calculated_returns, expected_returns, check_dtype=False)


if __name__ == "__main__":
    unittest.main()
