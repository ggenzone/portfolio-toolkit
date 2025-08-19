Multi-Currency Portfolio Examples
=================================

Portfolio Toolkit provides comprehensive support for multi-currency portfolios with automatic currency conversion and FIFO cost calculation.

Multi-Currency Portfolio Setup
------------------------------

Here's an example of a portfolio with transactions in multiple currencies:

.. code-block:: json

   {
     "name": "Multi Currency Portfolio",
     "currency": "EUR",
     "transactions": [
       {
         "ticker": null,
         "date": "2025-06-10",
         "type": "deposit",
         "quantity": 2000.00,
         "price": 1.00,
         "currency": "EUR",
         "total": 2000.00,
         "exchange_rate": 1.00,
         "subtotal_base": 2000.00,
         "fees_base": 0.00,
         "total_base": 2000.00
       },
       {
         "ticker": "AAPL",
         "date": "2025-06-12",
         "type": "buy",
         "quantity": 10,
         "price": 100.00,
         "currency": "USD",
         "total": 1000.00,
         "exchange_rate": 1.056,
         "subtotal_base": 947.00,
         "fees_base": 0.50,
         "total_base": 947.50
       },
       {
         "ticker": "SHOP",
         "date": "2025-06-13",
         "type": "buy",
         "quantity": 5,
         "price": 85.00,
         "currency": "CAD",
         "total": 425.00,
         "exchange_rate": 0.639,
         "subtotal_base": 271.58,
         "fees_base": 10.12,
         "total_base": 281.70
       }
     ]
   }

Working with Multi-Currency Data
--------------------------------

.. code-block:: python

   from portfolio_toolkit.portfolio.portfolio import Portfolio
   from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider

   # Load multi-currency portfolio
   data_provider = YFDataProvider()
   portfolio = Portfolio('examples/multi_currency_portfolio.json', data_provider)

   # Print positions (all values converted to base currency)
   portfolio.print_current_positions()

CLI Usage for Multi-Currency Portfolios
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also analyze multi-currency portfolios using the Portfolio Toolkit CLI:

.. code-block:: bash

   # Display current positions with automatic currency conversion
   portfolio-toolkit portfolio open-positions -f examples/multi_currency_portfolio.json

   # Plot portfolio evolution (all in base currency)
   portfolio-toolkit portfolio plot -f examples/multi_currency_portfolio.json

   # Export multi-currency data
   portfolio-toolkit portfolio export -f examples/multi_currency_portfolio.json --format csv

Exchange Rate Handling
----------------------

The system automatically handles currency conversion using the exchange rates specified in each transaction:

- **EUR/USD**: 1.056 (1 EUR = 1.056 USD)
- **EUR/CAD**: 0.639 (1 EUR = 0.639 CAD)

.. code-block:: python

   # The DataFrame shows both original and base currency values
   df = portfolio.df_portfolio
   
   # Check price columns
   print("Original Currency Prices:")
   print(df[['Ticker', 'Price', 'Currency']].drop_duplicates())
   
   print("\\nBase Currency Prices:")
   print(df[['Ticker', 'Price_Base', 'Value_Base']].drop_duplicates())

Expected Output:

.. code-block:: text

   Current positions as of 2025-07-14:
   | Ticker  | Price Base  | Cost        | Quantity  | Value Base  | Return (%)  |
   |---------|-----------|-----------|---------|-----------|-----------|
   | AAPL    | 197.56     | 947.50     | 10.00   | 1975.57   | 108.50    |
   | SHOP    | 81.92      | 281.70     | 5.00    | 409.61    | 45.41     |
   | __EUR   | 1.00       | 770.80     | 770.80  | 770.80    | 0.00      |
   |---------|-----------|-----------|---------|-----------|-----------|
   | TOTAL   |            | 2000.00    |         | 3155.98   | 57.80     |

Currency Conversion Mechanics
----------------------------

Understanding how currency conversion works:

1. **Transaction Level**: Each transaction specifies its original currency and exchange rate
2. **Automatic Conversion**: All amounts are automatically converted to the portfolio's base currency
3. **Fee Handling**: Fees are converted and included in the total cost basis
4. **Cash Tracking**: The system automatically creates synthetic cash transactions

.. code-block:: python

   # Example of how conversion works
   # Original: 10 AAPL @ $100 USD = $1000 USD
   # Exchange Rate: 1.056 (EUR/USD)
   # Converted: €947.00 EUR (before fees)
   # With fees: €947.50 EUR total cost

   # This is automatically handled by the preprocesador
   transaction = {
       "ticker": "AAPL",
       "quantity": 10,
       "price": 100.00,  # USD
       "currency": "USD",
       "total": 1000.00,  # USD
       "exchange_rate": 1.056,
       "subtotal_base": 947.00,  # EUR
       "fees_base": 0.50,  # EUR
       "total_base": 947.50  # EUR (final cost)
   }

FIFO Cost Calculation with Multiple Currencies
----------------------------------------------

The FIFO calculation works seamlessly across currencies:

.. code-block:: python

   # Example: Buy AAPL in USD, then sell in USD
   # All costs are tracked in base currency (EUR)
   
   from datetime import datetime
   
   # Check FIFO calculation after partial sale
   remaining_quantity = portfolio.calculate_current_quantity("AAPL", datetime(2025, 7, 14))
   print(f"Remaining AAPL shares: {remaining_quantity}")
   
   # The cost basis is maintained in EUR regardless of transaction currency

Advanced Multi-Currency Analysis
--------------------------------

.. code-block:: python

   def analyze_currency_exposure(portfolio):
       """Analyze currency exposure in the portfolio."""
       
       # Get the underlying DataFrame
       df = portfolio.df_portfolio
       
       # Group by currency (from original transactions)
       currency_exposure = {}
       
       for asset in portfolio.assets:
           ticker = asset["ticker"]
           if not portfolio.is_cash_ticker(ticker):
               # Get the original currency for this asset
               transactions = asset["transactions"]
               if transactions:
                   currency = transactions[0]["currency"]
                   current_qty = portfolio.calculate_current_quantity(ticker, datetime.now())
                   
                   # Get current value in base currency
                   latest_data = df[df['Ticker'] == ticker].iloc[-1]
                   current_value = latest_data['Value_Base']
                   
                   if currency not in currency_exposure:
                       currency_exposure[currency] = 0
                   currency_exposure[currency] += current_value
       
       return currency_exposure

   # Usage
   exposure = analyze_currency_exposure(portfolio)
   print("Currency Exposure (in base currency):")
   for currency, value in exposure.items():
       print(f"{currency}: {value:.2f} {portfolio.currency}")

Custom Exchange Rates
---------------------

You can specify custom exchange rates for each transaction:

.. code-block:: json

   {
     "ticker": "TSM",
     "date": "2025-06-14",
     "type": "buy",
     "quantity": 100,
     "price": 25.50,
     "currency": "TWD",
     "total": 2550.00,
     "exchange_rate": 0.031,
     "subtotal_base": 79.05,
     "fees_base": 0.95,
     "total_base": 80.00
   }

Tips for Multi-Currency Portfolios
----------------------------------

1. **Consistent Base Currency**: Always use the same base currency for your portfolio
2. **Accurate Exchange Rates**: Use accurate exchange rates from the transaction date
3. **Fee Conversion**: Convert fees to the base currency for accurate cost tracking
4. **Regular Updates**: Update exchange rates regularly for current valuations

Migration from Single Currency
------------------------------

If you have an existing single-currency portfolio and want to add multi-currency support:

.. code-block:: python

   # Original single-currency transaction
   old_transaction = {
       "ticker": "AAPL",
       "date": "2025-06-12",
       "type": "buy",
       "quantity": 10,
       "price": 100.00,
       "fees": 0.50
   }
   
   # Convert to multi-currency format
   new_transaction = {
       "ticker": "AAPL",
       "date": "2025-06-12",
       "type": "buy",
       "quantity": 10,
       "price": 100.00,
       "currency": "USD",  # Add currency
       "total": 1000.00,
       "exchange_rate": 1.056,  # Add exchange rate
       "subtotal_base": 947.00,  # Calculate base amounts
       "fees_base": 0.47,  # Convert fees
       "total_base": 947.47
   }

Use the migration script provided to automate this conversion:

.. code-block:: bash

   python migrate_v1_to_v2.py old_portfolio.json new_portfolio.json --add-cash --currency EUR
