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
        cls.cli_module = "cli.cli"

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

    def test_composition_help(self):
        self.assertTrue(self.run_command(["composition", "--help"], "Composition command help"))

    def test_correlation_help(self):
        self.assertTrue(self.run_command(["correlation", "--help"], "Correlation command help"))

    def test_plot_help(self):
        self.assertTrue(self.run_command(["plot", "--help"], "Plot command help"))

    def test_plot_portfolio_help(self):
        self.assertTrue(self.run_command(["plot-portfolio", "--help"], "Plot portfolio command help"))

    def test_print_positions_help(self):
        self.assertTrue(self.run_command(["print-positions", "--help"], "Print positions command help"))

    def test_export_transactions_help(self):
        self.assertTrue(self.run_command(["export-transactions", "--help"], "Export transactions command help"))

    def test_dump_data_frame_help(self):
        self.assertTrue(self.run_command(["dump-data-frame", "--help"], "Dump data frame command help"))

    def test_clear_cache_help(self):
        self.assertTrue(self.run_command(["clear-cache", "--help"], "Clear cache command help"))

    def test_ticker_info_help(self):
        self.assertTrue(self.run_command(["ticker-info", "--help"], "Ticker info command help"))

    def test_convert_currency_help(self):
        self.assertTrue(self.run_command(["convert-currency", "--help"], "Convert currency command help"))

    def test_clear_cache_execution(self):
        self.assertTrue(self.run_command(["clear-cache"], "Clear cache execution"))


if __name__ == "__main__":
    unittest.main()
