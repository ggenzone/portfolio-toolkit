#!/usr/bin/env python3

import sys
import os
# Add the parent directory to the path to import portfolio_tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from portfolio_tools.portfolio.portfolio import Portfolio

def test_print_transactions():
    """Test the new print_transactions functionality."""
    
    # Initialize data provider
    data_provider = YFDataProvider()
    
    # Get the path to the portfolio example file (in tests/examples/)
    portfolio_file = os.path.join(os.path.dirname(__file__), '..', 'examples', 'test_portfolio_v2.json')

    # Load portfolio v2
    portfolio = Portfolio(portfolio_file, data_provider)
    
    print("\n" + "="*80)
    print("TESTING print_transactions() METHOD")
    print("="*80)
    
    # Print transactions in CSV format
    portfolio.print_transactions()

if __name__ == "__main__":
    test_print_transactions()
