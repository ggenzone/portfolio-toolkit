Basic Usage Examples
====================

This section provides basic examples of how to use Portfolio Toolkit.

Loading a Portfolio
-------------------

.. code-block:: python

   from portfolio_toolkit.portfolio.portfolio import Portfolio
   from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider

   # Create a Yahoo Finance data provider
   data_provider = YFDataProvider()

   # Load portfolio from JSON file
   portfolio = Portfolio('examples/basic_portfolio.json', data_provider)

   # Print basic portfolio information
   print(f"Portfolio Name: {portfolio.name}")
   print(f"Base Currency: {portfolio.currency}")
   print(f"Number of Assets: {len(portfolio.assets)}")

Viewing Current Positions
-------------------------

.. code-block:: python

   # Print current positions (latest available date)
   portfolio.print_current_positions()

   # Print positions for a specific date
   from datetime import datetime
   portfolio.print_current_positions(datetime(2025, 6, 15))

Example Output:

.. code-block:: text

   Current positions as of 2025-07-14:
   | Ticker  | Price Base  | Cost        | Quantity  | Value Base  | Return (%)  |
   |---------|-----------|-----------|---------|-----------|-----------|
   | AAPL    | 208.62     | 500.25     | 5.00    | 1043.10   | 108.52    |
   | __EUR   | 1.00       | 499.75     | 499.75  | 499.75    | 0.00      |
   |---------|-----------|-----------|---------|-----------|-----------|
   | TOTAL   |            | 1000.00    |         | 1542.85   | 54.28     |

Calculating Portfolio Metrics
-----------------------------

.. code-block:: python

   # Calculate current quantity of an asset
   aapl_quantity = portfolio.calculate_current_quantity("AAPL", datetime(2025, 7, 14))
   print(f"Current AAPL quantity: {aapl_quantity}")

   # Calculate portfolio value evolution
   dates, values = portfolio.calculate_value()
   print(f"Portfolio value on {dates[-1]}: {values[-1]:.2f}")

Exporting Data
--------------

.. code-block:: python

   # Print all transactions
   portfolio.print_transactions()

   # Print the underlying DataFrame for debugging
   portfolio.print_data_frame()

Plotting Portfolio Data
-----------------------

.. code-block:: python

   # Plot portfolio composition
   portfolio.plot_composition()

   # Plot portfolio evolution over time
   portfolio.plot_evolution()

   # Plot portfolio evolution vs cost
   portfolio.plot_evolution_vs_cost()

   # Plot evolution for a specific ticker
   portfolio.plot_evolution_ticker("AAPL")

Working with Cash Transactions
------------------------------

.. code-block:: python

   # Get cash transactions only
   cash_transactions = portfolio.get_cash_transactions()
   print(f"Number of cash transactions: {len(cash_transactions)}")

   # Get stock assets only (excluding cash)
   stock_assets = portfolio.get_stock_assets()
   print(f"Number of stock assets: {len(stock_assets)}")

   # Check if a ticker is a cash ticker
   is_cash = portfolio.is_cash_ticker("__EUR")  # True
   is_stock = portfolio.is_cash_ticker("AAPL")  # False

Error Handling
--------------

.. code-block:: python

   try:
       portfolio = Portfolio('nonexistent.json', data_provider)
   except FileNotFoundError:
       print("Portfolio file not found")

   try:
       # This will fail if data provider can't fetch data
       invalid_portfolio = Portfolio('portfolio_with_invalid_ticker.json', data_provider)
   except Exception as e:
       print(f"Error loading portfolio: {e}")

Complete Example
----------------

Here's a complete example that loads a portfolio and performs various operations:

.. code-block:: python

   from portfolio_toolkit.portfolio.portfolio import Portfolio
   from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
   from datetime import datetime

   def analyze_portfolio(portfolio_path):
       # Initialize data provider and portfolio
       data_provider = YFDataProvider()
       portfolio = Portfolio(portfolio_path, data_provider)
       
       print(f"=== Portfolio Analysis: {portfolio.name} ===")
       print(f"Base Currency: {portfolio.currency}")
       print(f"Number of Assets: {len(portfolio.assets)}")
       print()
       
       # Show current positions
       print("Current Positions:")
       portfolio.print_current_positions()
       print()
       
       # Calculate total value
       dates, values = portfolio.calculate_value()
       if dates and values:
           print(f"Latest Portfolio Value: {values[-1]:.2f} {portfolio.currency}")
           print(f"Portfolio Start Date: {dates[0].strftime('%Y-%m-%d')}")
           print(f"Latest Data Date: {dates[-1].strftime('%Y-%m-%d')}")
       
       # Show asset breakdown
       stock_assets = portfolio.get_stock_assets()
       cash_transactions = portfolio.get_cash_transactions()
       
       print(f"Stock Assets: {len(stock_assets)}")
       print(f"Cash Transactions: {len(cash_transactions)}")
       
       return portfolio

   # Usage
   if __name__ == "__main__":
       portfolio = analyze_portfolio('tests/examples/basic_portfolio.json')
       
       # Generate plots
       portfolio.plot_composition()
       portfolio.plot_evolution()
