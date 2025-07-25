import unittest
import pandas as pd
from portfolio_toolkit.utils.correlation import calculate_correlation


class TestCorrelation(unittest.TestCase):
    """Test suite for the calculate_correlation function."""

    def test_calculate_correlation(self):
        """Test the calculation of correlation between two return series."""
        # Create sample return series
        returns1 = pd.Series([0.01, 0.02, 0.03, 0.04, 0.05])
        returns2 = pd.Series([0.05, 0.04, 0.03, 0.02, 0.01])

        # Expected correlation
        expected_correlation = returns1.corr(returns2)

        # Calculate correlation using the function
        calculated_correlation = calculate_correlation(returns1, returns2)

        # Assert that the calculated correlation matches the expected correlation
        self.assertAlmostEqual(calculated_correlation, expected_correlation, places=6)

    def test_empty_series(self):
        """Test the function with empty series."""
        returns1 = pd.Series(dtype=float)
        returns2 = pd.Series(dtype=float)
        calculated_correlation = calculate_correlation(returns1, returns2)
        self.assertTrue(pd.isna(calculated_correlation))

    def test_single_value_series(self):
        """Test the function with single value series."""
        returns1 = pd.Series([0.01])
        returns2 = pd.Series([0.02])
        calculated_correlation = calculate_correlation(returns1, returns2)
        self.assertTrue(pd.isna(calculated_correlation))

    def test_dataframe_input(self):
        """Test the function with DataFrame inputs instead of Series."""
        returns1 = pd.DataFrame([0.01, 0.02, 0.03, 0.04, 0.05])
        returns2 = pd.DataFrame([0.05, 0.04, 0.03, 0.02, 0.01])

        # Expected correlation
        expected_correlation = returns1.squeeze().corr(returns2.squeeze())

        # Calculate correlation using the function
        calculated_correlation = calculate_correlation(returns1, returns2)

        # Assert that the calculated correlation matches the expected correlation
        self.assertAlmostEqual(calculated_correlation, expected_correlation, places=6)


if __name__ == "__main__":
    unittest.main()
