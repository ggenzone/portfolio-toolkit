#!/usr/bin/env python3
"""
Script to validate all example portfolios work correctly with the portfolio system.
"""

import json
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from portfolio_toolkit.portfolio import Portfolio
from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider


def validate_portfolio(portfolio_path, expected_name, expected_currency):
    """Validate a single portfolio file"""
    print(f"\n=== Validating {os.path.basename(portfolio_path)} ===")
    
    try:
        # Create data provider
        data_provider = YFDataProvider()
        
        data = json.load(open(portfolio_path, 'r'))
        # Load portfolio
        basic_portfolio = Portfolio.from_dict(data, data_provider)
        portfolio = basic_portfolio.get_time_series()

        # Basic validation
        print(f"✓ Portfolio loaded successfully")
        print(f"  Name: {portfolio.name}")
        print(f"  Currency: {portfolio.currency}")
        print(f"  Assets: {len(portfolio.assets)}")
        
        # Validate expected values
        assert portfolio.name == expected_name, f"Expected name '{expected_name}', got '{portfolio.name}'"
        assert portfolio.currency == expected_currency, f"Expected currency '{expected_currency}', got '{portfolio.currency}'"
        print(f"✓ Basic properties validated")
        
        # Try to get DataFrame
        df = portfolio.portfolio_timeseries
        if df is not None:
            print(f"✓ DataFrame generated successfully ({len(df)} rows)")
        else:
            print(f"⚠ DataFrame is None")
        
        # Check required columns
        required_columns = ['Date', 'Ticker', 'Quantity', 'Price', 'Price_Base', 'Value', 'Value_Base', 'Cost', 'Sector', 'Country']
        for col in required_columns:
            assert col in df.columns, f"Missing required column: {col}"
        print(f"✓ Required columns present")
        
        # Try printing current positions
        # print(f"✓ Current positions:")
        # portfolio.print_current_positions()
        
        return True
        
    except Exception as e:
        print(f"✗ Error validating {portfolio_path}: {str(e)}")
        return False


def main():
    """Main validation function"""
    print("Portfolio Tools - Example Validation")
    print("=" * 50)
    
    # Get examples directory
    examples_dir = os.path.join(os.path.dirname(__file__), "portfolio")
    
    if not os.path.exists(examples_dir):
        print(f"✗ Examples directory not found: {examples_dir}")
        return False
    
    # Define test cases
    test_cases = [
        ("basic_portfolio.json", "Basic Portfolio Test", "EUR"),
        ("multi_currency_portfolio.json", "Multi Currency Portfolio Test", "EUR"),
        ("fifo_test_portfolio.json", "FIFO Test Portfolio", "EUR"),
        # ("cash_only_portfolio.json", "Cash Only Portfolio Test", "EUR"),
        ("test_portfolio_v2.json", "Test Portfolio", "EUR")
    ]
    
    results = []
    
    for filename, expected_name, expected_currency in test_cases:
        portfolio_path = os.path.join(examples_dir, filename)
        
        if not os.path.exists(portfolio_path):
            print(f"\n✗ Portfolio file not found: {portfolio_path}")
            results.append(False)
            continue
        
        success = validate_portfolio(portfolio_path, expected_name, expected_currency)
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
