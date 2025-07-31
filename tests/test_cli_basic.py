"""
Quick test runner for CLI functionality.

This script provides a simple way to verify that the CLI refactoring is working
correctly without requiring a full test suite setup.
"""

import unittest
import subprocess
import sys
from pathlib import Path


class TestCLIBasic(unittest.TestCase):
    """Test suite for basic CLI functionality after Click refactoring."""

    @classmethod
    def setUpClass(cls):
        cls.project_root = Path(__file__).parent.parent
        cls.cli_module = "portfolio_toolkit.cli.cli"

    def run_command(self, args, description):
        """Run a CLI command and check if it succeeds."""
        cmd = [sys.executable, "-m", self.cli_module] + args
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.project_root),
                timeout=10
            )

            if result.returncode == 0:
                print(f"✅ {description}")
                return True
            else:
                print(f"❌ {description}")
                print(f"   Error: {result.stderr.strip()}")
                return False

        except subprocess.TimeoutExpired:
            print(f"⏰ {description} (timeout)")
            return False
        except Exception as e:
            print(f"💥 {description} (exception: {e})")
            return False

    def test_main_help(self):
        self.assertTrue(self.run_command(["--help"], "Main CLI help"))

    def test_version_display(self):
        self.assertTrue(self.run_command(["--version"], "Version display"))

    def test_ticker_help(self):
        self.assertTrue(self.run_command(["ticker", "--help"], "Ticker command help"))

    def test_ticker_print_help(self):
        self.assertTrue(self.run_command(["ticker", "print", "--help"], "Ticker print command help"))

    def test_ticker_correlation_help(self):
        self.assertTrue(self.run_command(["ticker", "correlation", "--help"], "Ticker correlation command help"))

    def test_portfolio_help(self):
        self.assertTrue(self.run_command(["portfolio", "--help"], "Portfolio command help"))

    def test_portfolio_transactions_help(self):
        self.assertTrue(self.run_command(["portfolio", "transactions", "--help"], "Portfolio transactions command help"))

    def test_portfolio_positions_help(self):
        self.assertTrue(self.run_command(["portfolio", "positions", "--help"], "Portfolio positions command help"))

    def test_portfolio_evolution_help(self):
        self.assertTrue(self.run_command(["portfolio", "evolution", "--help"], "Portfolio evolution command help"))

    def test_optimization_help(self):
        self.assertTrue(self.run_command(["optimization", "--help"], "Optimization command help"))

    def test_clear_cache_help(self):
        self.assertTrue(self.run_command(["clear-cache", "--help"], "Clear cache command help"))

    def test_clear_cache_execution(self):
        self.assertTrue(self.run_command(["clear-cache"], "Clear cache execution"))


if __name__ == "__main__":
    unittest.main()
