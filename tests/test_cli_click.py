"""
Test suite for the new organized CLI structure.

This module tests that all CLI commands work correctly with the new organized structure:
- ticker: Ticker analysis commands
- watchlist: Watchlist analysis commands  
- optimization: Portfolio optimization commands
- portfolio: Portfolio analysis commands
"""

import unittest
import subprocess
import sys
import os
import tempfile
import json
from pathlib import Path


class TestNewCLI(unittest.TestCase):
    """Test suite for the new organized CLI structure."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""  
        cls.project_root = Path(__file__).parent.parent
        cls.cli_module = "portfolio_toolkit.cli.cli"
        
        # Create a sample portfolio file for testing
        cls.sample_portfolio = {
            "name": "Test Portfolio",
            "currency": "USD",
            "assets": [
                {
                    "ticker": "AAPL",
                    "transactions": [
                        {
                            "date": "2023-01-01",
                            "type": "buy",
                            "quantity": 10,
                            "price": 150.0
                        }
                    ]
                }
            ]
        }
        
        # Create temporary portfolio file
        cls.temp_portfolio = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(cls.sample_portfolio, cls.temp_portfolio)
        cls.temp_portfolio.close()

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        if hasattr(cls, 'temp_portfolio'):
            os.unlink(cls.temp_portfolio.name)

    def run_cli_command(self, command_args, expect_success=True):
        """
        Run a CLI command and return the result.
        
        Args:
            command_args (list): List of command arguments
            expect_success (bool): Whether to expect the command to succeed
            
        Returns:
            subprocess.CompletedProcess: The result of the command
        """
        cmd = [sys.executable, "-m", self.cli_module] + command_args
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(self.project_root)
        )
        
        if expect_success:
            self.assertEqual(result.returncode, 0, 
                           f"Command failed: {' '.join(cmd)}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
        
        return result

    def test_main_cli_help(self):
        """Test that the main CLI shows help correctly."""
        result = self.run_cli_command(["--help"])
        
        self.assertIn("Portfolio Toolkit CLI", result.stdout)
        self.assertIn("Manage and analyze your investment portfolios", result.stdout)
        self.assertIn("Commands:", result.stdout)
        
        # Check that all expected command groups are listed
        expected_commands = [
            "ticker", "optimization", "portfolio", "clear-cache"
        ]
        
        for command in expected_commands:
            self.assertIn(command, result.stdout, f"Command group {command} not found in help output")

    def test_version_option(self):
        """Test the --version option."""
        result = self.run_cli_command(["--version"])
        # Just check that it runs without error, version output format may vary
        self.assertEqual(result.returncode, 0)

    # Ticker Command Tests
    def test_ticker_help(self):
        """Test ticker command group help."""
        result = self.run_cli_command(["ticker", "--help"])
        
        self.assertIn("Ticker analysis commands", result.stdout)
        self.assertIn("print", result.stdout)
        self.assertIn("plot", result.stdout)
        self.assertIn("export", result.stdout)
        self.assertIn("compare", result.stdout)

    def test_ticker_print_help(self):
        """Test ticker print subcommand help."""
        result = self.run_cli_command(["ticker", "print", "--help"])
        
        self.assertIn("Print ticker information", result.stdout)
        self.assertIn("info", result.stdout)
        self.assertIn("stats", result.stdout)
        self.assertIn("beta", result.stdout)

    def test_ticker_print_info_help(self):
        """Test ticker print info command help."""
        result = self.run_cli_command(["ticker", "print", "info", "--help"])
        
        self.assertIn("Show detailed ticker information", result.stdout)
        self.assertIn("SYMBOL", result.stdout)

    def test_ticker_print_info_implemented(self):
        """Test ticker print info works (shows real data, not 'not implemented')."""
        result = self.run_cli_command(["ticker", "print", "info", "AAPL"])
        
        # The ticker info command appears to be implemented
        self.assertIn("AAPL", result.stdout)
        self.assertIn("Currency", result.stdout)

    def test_ticker_compare_help(self):
        """Test ticker compare command help."""
        result = self.run_cli_command(["ticker", "compare", "--help"])
        
        self.assertIn("Compare multiple tickers", result.stdout)
        self.assertIn("SYMBOLS", result.stdout)

    def test_ticker_compare_not_implemented(self):
        """Test ticker compare shows not implemented message."""
        result = self.run_cli_command(["ticker", "compare", "AAPL", "MSFT"])
        
        self.assertIn("not implemented yet", result.stdout)
        self.assertIn("ticker compare AAPL MSFT", result.stdout)

    def test_ticker_plot_help(self):
        """Test ticker plot subcommand help."""
        result = self.run_cli_command(["ticker", "plot", "--help"])
        
        self.assertIn("Plot ticker data", result.stdout)
        self.assertIn("returns-distribution", result.stdout)
        self.assertIn("volatility", result.stdout)

    def test_ticker_export_help(self):
        """Test ticker export subcommand help."""
        result = self.run_cli_command(["ticker", "export", "--help"])
        
        self.assertIn("Export ticker data", result.stdout)
        self.assertIn("data", result.stdout)

    # Portfolio Command Tests
    def test_portfolio_help(self):
        """Test portfolio command group help."""
        result = self.run_cli_command(["portfolio", "--help"])
        
        self.assertIn("Portfolio analysis commands", result.stdout)
        self.assertIn("transactions", result.stdout)
        self.assertIn("positions", result.stdout)
        self.assertIn("evolution", result.stdout)
        self.assertIn("performance", result.stdout)
        self.assertIn("tax-report", result.stdout)

    def test_portfolio_transactions_help(self):
        """Test portfolio transactions subcommand help."""
        result = self.run_cli_command(["portfolio", "transactions", "--help"])
        
        self.assertIn("Show portfolio transactions", result.stdout)
        self.assertIn("FILE", result.stdout)

    def test_portfolio_positions_help(self):
        """Test portfolio positions command help."""
        result = self.run_cli_command(["portfolio", "positions", "--help"])
        
        self.assertIn("Show open positions", result.stdout)
        self.assertIn("FILE", result.stdout)
        self.assertIn("DATE", result.stdout)

    def test_portfolio_evolution_help(self):
        """Test portfolio evolution subcommand help."""
        result = self.run_cli_command(["portfolio", "evolution", "--help"])
        
        self.assertIn("Plot portfolio value evolution", result.stdout)
        self.assertIn("FILE", result.stdout)

    def test_portfolio_performance_help(self):
        """Test portfolio performance subcommand help."""
        result = self.run_cli_command(["portfolio", "performance", "--help"])
        
        self.assertIn("Show performance summary", result.stdout)
        self.assertIn("FILE", result.stdout)

    def test_portfolio_tax_report_help(self):
        """Test portfolio tax-report subcommand help."""
        result = self.run_cli_command(["portfolio", "tax-report", "--help"])
        
        self.assertIn("Generate tax report", result.stdout)
        self.assertIn("FILE", result.stdout)
        self.assertIn("YEAR", result.stdout)

    # Optimization Command Tests
    def test_optimization_help(self):
        """Test optimization command group help."""
        result = self.run_cli_command(["optimization", "--help"])
        
        self.assertIn("Portfolio optimization commands", result.stdout)
        self.assertIn("plot", result.stdout)
        self.assertIn("calc", result.stdout)
        self.assertIn("print", result.stdout)
        self.assertIn("optimize", result.stdout)
        self.assertIn("export", result.stdout)
        self.assertIn("backtest", result.stdout)
        self.assertIn("risk", result.stdout)

    def test_optimization_plot_help(self):
        """Test optimization plot subcommand help."""
        result = self.run_cli_command(["optimization", "plot", "--help"])
        
        self.assertIn("Plot optimization data", result.stdout)
        self.assertIn("composition", result.stdout)
        self.assertIn("frontier", result.stdout)
        self.assertIn("correlation-matrix", result.stdout)

    def test_optimization_calc_help(self):
        """Test optimization calc subcommand help."""
        result = self.run_cli_command(["optimization", "calc", "--help"])
        
        self.assertIn("Calculate optimization metrics", result.stdout)
        self.assertIn("var", result.stdout)

    # Legacy Commands (should still work)
    def test_clear_cache_help(self):
        """Test clear-cache command help."""
        result = self.run_cli_command(["clear-cache", "--help"])
        
        self.assertIn("Delete all cache files in temp/*.pkl", result.stdout)

    def test_clear_cache_execution(self):
        """Test clear-cache command execution (safe to run)."""
        result = self.run_cli_command(["clear-cache"])
        
        # Should run without error even if no cache files exist
        self.assertEqual(result.returncode, 0)

    # Error Handling Tests
    def test_invalid_command(self):
        """Test that invalid commands show appropriate error."""
        result = self.run_cli_command(["invalid-command"], expect_success=False)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No such command", result.stderr)

    def test_ticker_missing_argument(self):
        """Test ticker print info with missing symbol argument."""
        result = self.run_cli_command(["ticker", "print", "info"], expect_success=False)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing argument", result.stderr)

    def test_portfolio_missing_file_argument(self):
        """Test portfolio positions with missing file argument."""
        result = self.run_cli_command(["portfolio", "positions"], expect_success=False)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing argument", result.stderr)

    def test_command_with_nonexistent_file(self):
        """Test that commands requiring files validate correctly."""
        # Test with non-existent file
        result = self.run_cli_command(["portfolio", "open-positions", "non_existent_file.json", "2024-01-01"], expect_success=False)
        
        # The command should fail during execution
        self.assertNotEqual(result.returncode, 0)


class TestCLIIntegration(unittest.TestCase):
    """Integration tests that require network access and external data."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.project_root = Path(__file__).parent.parent
        cls.cli_module = "cli.cli"

    def run_cli_command(self, command_args, timeout=30):
        """
        Run a CLI command and return the result.
        
        Args:
            command_args (list): List of command arguments
            timeout (int): Timeout in seconds
            
        Returns:
            subprocess.CompletedProcess: The result of the command
        """
        cmd = [sys.executable, "-m", self.cli_module] + command_args
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(self.project_root),
            timeout=timeout
        )
        
        return result

    @unittest.skip("Requires network access - run manually when needed")
    def test_ticker_info_implementation(self):
        """Test when ticker commands are implemented (requires network)."""
        result = self.run_cli_command(["ticker", "print", "info", "AAPL"])
        
        # For now, all commands show "not implemented"
        self.assertIn("not implemented yet", result.stdout)


def run_cli_smoke_tests():
    """
    Run basic smoke tests to ensure CLI is working.
    This function can be called independently for quick testing.
    """
    print("Running CLI smoke tests...")
    
    project_root = Path(__file__).parent.parent
    cli_module = "cli.cli"
    
    def run_command(args):
        cmd = [sys.executable, "-m", cli_module] + args
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(project_root))
        return result.returncode == 0, result.stdout, result.stderr
    
    tests = [
        (["--help"], "Main help"),
        (["--version"], "Version"),
        (["ticker", "--help"], "Ticker help"),
        (["ticker", "print", "--help"], "Ticker print help"),
        (["portfolio", "--help"], "Portfolio help"),
        (["portfolio", "print", "--help"], "Portfolio print help"),
        (["watchlist", "--help"], "Watchlist help"),
        (["optimization", "--help"], "Optimization help"),
        (["clear-cache"], "Clear cache"),
        (["ticker", "print", "info", "AAPL"], "Ticker info (not implemented)"),
        (["ticker", "compare", "AAPL", "MSFT"], "Ticker compare (not implemented)"),
    ]
    
    passed = 0
    failed = 0
    
    for args, description in tests:
        success, stdout, stderr = run_command(args)
        if success:
            print(f"✅ {description}")
            passed += 1
        else:
            print(f"❌ {description}: {stderr}")
            failed += 1
    
    print(f"\nSmoke tests completed: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the new CLI structure")
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests only")
    parser.add_argument("--integration", action="store_true", help="Include integration tests (requires network)")
    args = parser.parse_args()
    
    if args.smoke:
        success = run_cli_smoke_tests()
        sys.exit(0 if success else 1)
    else:
        # Run unit tests
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestNewCLI)
        
        if args.integration:
            suite.addTests(loader.loadTestsFromTestCase(TestCLIIntegration))
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        sys.exit(0 if result.wasSuccessful() else 1)
