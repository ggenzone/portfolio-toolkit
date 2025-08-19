#!/usr/bin/env python3
"""
Script to validate all example watchlists work correctly with the portfolio system.
"""

import json
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from portfolio_toolkit.watchlist import Watchlist
from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider


def validate_watchlist(watchlist_path, expected_name, expected_currency):
    """Validate a single watchlist file"""
    print(f"\n=== Validating {os.path.basename(watchlist_path)} ===")

    try:
        # Create data provider
        data_provider = YFDataProvider()

        data = json.load(open(watchlist_path, 'r'))
        # Load watchlist
        watchlist = Watchlist.from_dict(data, data_provider)

        # Basic validation
        print(f"✓ Watchlist loaded successfully")
        print(f"  Name: {watchlist.name}")
        print(f"  Currency: {watchlist.currency}")
        print(f"  Assets: {len(watchlist.assets)}")
        
        # Validate expected values
        assert watchlist.name == expected_name, f"Expected name '{expected_name}', got '{watchlist.name}'"
        assert watchlist.currency == expected_currency, f"Expected currency '{expected_currency}', got '{watchlist.currency}'"
        print(f"✓ Basic properties validated")
        
        return True
        
    except Exception as e:
        print(f"✗ Error validating {watchlist_path}: {str(e)}")
        return False


def main():
    """Main validation function"""
    print("Watchlist Tools - Example Validation")
    print("=" * 50)
    
    # Get examples directory
    examples_dir = os.path.join(os.path.dirname(__file__), "watchlist")

    if not os.path.exists(examples_dir):
        print(f"✗ Examples directory not found: {examples_dir}")
        return False
    
    # Define test cases
    test_cases = [
        ("basic_watchlist.json", "Technology Sector ETFs (EUR)", "EUR"),
        ("basic_watchlist_without_currency.json", "Technology Sector ETFs", None)
    ]
    
    results = []
    
    for filename, expected_name, expected_currency in test_cases:
        watchlist_path = os.path.join(examples_dir, filename)

        if not os.path.exists(watchlist_path):
            print(f"\n✗ Watchlist file not found: {watchlist_path}")
            results.append(False)
            continue

        success = validate_watchlist(watchlist_path, expected_name, expected_currency)
        results.append(success)
    
    # Summary
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(results)
    failed_tests = total_tests - passed_tests
    
    print(f"Total portfolios tested: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    
    if failed_tests == 0:
        print("✓ All portfolios validated successfully!")
        return True
    else:
        print(f"✗ {failed_tests} portfolio(s) failed validation")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
