#!/usr/bin/env python3
"""
Test suite for the Click-based CLI refactoring.

This module tests that all CLI commands work correctly after the migration
from argparse to Click.
"""

import unittest
import subprocess
import sys
import os
import tempfile
import json
from pathlib import Path


class TestClickCLI(unittest.TestCase):
    """Test suite for the Click-based CLI."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.project_root = Path(__file__).parent.parent
        cls.cli_module = "cli.cli"
        
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
        
        self.assertIn("Portfolio Tools CLI", result.stdout)
        self.assertIn("Manage and analyze your investment portfolios", result.stdout)
        self.assertIn("Commands:", result.stdout)
        
        # Check that all expected commands are listed
        expected_commands = [
            "composition", "correlation", "plot", "plot-portfolio",
            "print-positions", "export-transactions", "dump-data-frame",
            "clear-cache", "ticker-info", "convert-currency"
        ]
        
        for command in expected_commands:
            self.assertIn(command, result.stdout, f"Command {command} not found in help output")

    def test_version_option(self):
        """Test the --version option."""
        result = self.run_cli_command(["--version"])
        # Just check that it runs without error, version output format may vary
        self.assertEqual(result.returncode, 0)

    def test_composition_help(self):
        """Test composition command help."""
        result = self.run_cli_command(["composition", "--help"])
        
        self.assertIn("Plot the portfolio composition", result.stdout)
        self.assertIn("-f, --file", result.stdout)
        self.assertIn("Portfolio file in JSON format", result.stdout)

    def test_correlation_help(self):
        """Test correlation command help."""
        result = self.run_cli_command(["correlation", "--help"])
        
        self.assertIn("Calculate correlation between asset pairs", result.stdout)
        self.assertIn("-t, --tickers", result.stdout)
        self.assertIn("Comma-separated list of tickers", result.stdout)

    def test_plot_help(self):
        """Test plot command help."""
        result = self.run_cli_command(["plot", "--help"])
        
        self.assertIn("Plot the price evolution of a list of assets", result.stdout)
        self.assertIn("TICKERS", result.stdout)
        self.assertIn("CURRENCY", result.stdout)

    def test_plot_portfolio_help(self):
        """Test plot-portfolio command help."""
        result = self.run_cli_command(["plot-portfolio", "--help"])
        
        self.assertIn("Plot the portfolio evolution", result.stdout)
        self.assertIn("-f, --file", result.stdout)

    def test_print_positions_help(self):
        """Test print-positions command help."""
        result = self.run_cli_command(["print-positions", "--help"])
        
        self.assertIn("Print current portfolio positions as a table", result.stdout)
        self.assertIn("-f, --file", result.stdout)
        self.assertIn("-d, --date", result.stdout)

    def test_export_transactions_help(self):
        """Test export-transactions command help."""
        result = self.run_cli_command(["export-transactions", "--help"])
        
        self.assertIn("Export all portfolio transactions in CSV format", result.stdout)
        self.assertIn("-f, --file", result.stdout)

    def test_dump_data_frame_help(self):
        """Test dump-data-frame command help."""
        result = self.run_cli_command(["dump-data-frame", "--help"])
        
        self.assertIn("Dump portfolio DataFrame for debugging purposes", result.stdout)
        self.assertIn("-f, --file", result.stdout)

    def test_clear_cache_help(self):
        """Test clear-cache command help."""
        result = self.run_cli_command(["clear-cache", "--help"])
        
        self.assertIn("Delete all cache files in temp/*.pkl", result.stdout)

    def test_ticker_info_help(self):
        """Test ticker-info command help."""
        result = self.run_cli_command(["ticker-info", "--help"])
        
        self.assertIn("Show detailed ticker information", result.stdout)
        self.assertIn("TICKER", result.stdout)

    def test_convert_currency_help(self):
        """Test convert-currency command help."""
        result = self.run_cli_command(["convert-currency", "--help"])
        
        self.assertIn("Convert ticker prices to different currency", result.stdout)
        self.assertIn("TICKER", result.stdout)
        self.assertIn("CURRENCY", result.stdout)
        self.assertIn("--days", result.stdout)

    def test_invalid_command(self):
        """Test that invalid commands show appropriate error."""
        result = self.run_cli_command(["invalid-command"], expect_success=False)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No such command", result.stderr)

    def test_missing_required_option(self):
        """Test that missing required options show appropriate error."""
        result = self.run_cli_command(["composition"], expect_success=False)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing option", result.stderr)

    def test_clear_cache_execution(self):
        """Test clear-cache command execution (safe to run)."""
        result = self.run_cli_command(["clear-cache"])
        
        # Should run without error even if no cache files exist
        self.assertEqual(result.returncode, 0)

    def test_ticker_info_missing_argument(self):
        """Test ticker-info command with missing ticker argument."""
        result = self.run_cli_command(["ticker-info"], expect_success=False)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing argument", result.stderr)

    def test_convert_currency_missing_arguments(self):
        """Test convert-currency command with missing arguments."""
        result = self.run_cli_command(["convert-currency"], expect_success=False)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing argument", result.stderr)

    def test_plot_missing_arguments(self):
        """Test plot command with missing arguments."""
        result = self.run_cli_command(["plot"], expect_success=False)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing argument", result.stderr)

    def test_command_with_file_option_validation(self):
        """Test that commands requiring file options validate correctly."""
        # Test with non-existent file
        result = self.run_cli_command(["composition", "-f", "non_existent_file.json"], expect_success=False)
        
        # The command should fail during execution, not during parsing
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
    def test_ticker_info_real_ticker(self):
        """Test ticker-info with a real ticker (requires network)."""
        result = self.run_cli_command(["ticker-info", "AAPL"])
        
        if result.returncode == 0:
            self.assertIn("AAPL", result.stdout)
            self.assertIn("Currency:", result.stdout)
        else:
            # Network issues are acceptable in automated tests
            self.assertIn("Error", result.stdout)

    @unittest.skip("Requires network access - run manually when needed")
    def test_convert_currency_real_ticker(self):
        """Test convert-currency with a real ticker (requires network)."""
        result = self.run_cli_command(["convert-currency", "AAPL", "EUR", "--days", "3"])
        
        if result.returncode == 0:
            self.assertIn("Converting AAPL", result.stdout)
            self.assertIn("EUR", result.stdout)
        else:
            # Network issues are acceptable in automated tests
            self.assertIn("Error", result.stdout)

    @unittest.skip("Requires network access - run manually when needed")
    def test_correlation_real_tickers(self):
        """Test correlation with real tickers (requires network)."""
        result = self.run_cli_command(["correlation", "-t", "AAPL,MSFT"])
        
        if result.returncode == 0:
            self.assertIn("AAPL", result.stdout)
            self.assertIn("MSFT", result.stdout)
            self.assertIn("Correlation", result.stdout)
        else:
            # Network issues are acceptable in automated tests
            self.assertIn("Error", result.stdout)


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
        (["composition", "--help"], "Composition help"),
        (["correlation", "--help"], "Correlation help"),
        (["plot", "--help"], "Plot help"),
        (["ticker-info", "--help"], "Ticker info help"),
        (["clear-cache"], "Clear cache"),
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
    
    parser = argparse.ArgumentParser(description="Test the CLI refactoring")
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests only")
    parser.add_argument("--integration", action="store_true", help="Include integration tests (requires network)")
    args = parser.parse_args()
    
    if args.smoke:
        success = run_cli_smoke_tests()
        sys.exit(0 if success else 1)
    else:
        # Run unit tests
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestClickCLI)
        
        if args.integration:
            suite.addTests(loader.loadTestsFromTestCase(TestCLIIntegration))
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        sys.exit(0 if result.wasSuccessful() else 1)
