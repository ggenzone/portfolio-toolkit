#!/usr/bin/env python3
"""
Quick test runner for CLI functionality.

This script provides a simple way to verify that the CLI refactoring is working
correctly without requiring a full test suite setup.
"""

import subprocess
import sys
from pathlib import Path


def test_cli_basic_functionality():
    """Test basic CLI functionality after Click refactoring."""
    
    project_root = Path(__file__).parent.parent
    cli_module = "cli.cli"
    
    print("🧪 Testing CLI refactoring...")
    print("=" * 50)
    
    def run_command(args, description):
        """Run a CLI command and check if it succeeds."""
        cmd = [sys.executable, "-m", cli_module] + args
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                cwd=str(project_root),
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
    
    # Test cases: (command_args, description)
    tests = [
        (["--help"], "Main CLI help"),
        (["--version"], "Version display"),
        (["composition", "--help"], "Composition command help"),
        (["correlation", "--help"], "Correlation command help"),
        (["plot", "--help"], "Plot command help"),
        (["plot-portfolio", "--help"], "Plot portfolio command help"),
        (["print-positions", "--help"], "Print positions command help"),
        (["export-transactions", "--help"], "Export transactions command help"),
        (["dump-data-frame", "--help"], "Dump data frame command help"),
        (["clear-cache", "--help"], "Clear cache command help"),
        (["ticker-info", "--help"], "Ticker info command help"),
        (["convert-currency", "--help"], "Convert currency command help"),
        (["clear-cache"], "Clear cache execution"),
    ]
    
    passed = 0
    failed = 0
    
    for args, description in tests:
        if run_command(args, description):
            passed += 1
        else:
            failed += 1
    
    print("=" * 50)
    print(f"📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All CLI tests passed! The refactoring is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the CLI implementation.")
    
    assert failed == 0, f"CLI tests failed: {failed} out of {passed + failed}"


if __name__ == "__main__":
    test_cli_basic_functionality()
