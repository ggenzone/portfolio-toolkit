CLI Usage Examples
==================

This section provides comprehensive examples of how to use the Portfolio Tools command-line interface (CLI). The CLI has been built using the Click framework for an intuitive and user-friendly experience.

Installation and Quick Start
-----------------------------

After installing the package, you can access the CLI directly:

.. code-block:: bash

   # Install the package
   pip install -e .

   # View available commands
   portfolio-tools --help

   # Check version
   portfolio-tools --version

Basic Commands
--------------

Help and Information
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Main help
   portfolio-tools --help

   # Help for specific command
   portfolio-tools composition --help
   portfolio-tools plot --help

Version Information
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Show version
   portfolio-tools --version

Portfolio Analysis Commands
---------------------------

Portfolio Composition
~~~~~~~~~~~~~~~~~~~~~~

Analyze and visualize portfolio composition by different criteria:

.. code-block:: bash

   # Basic composition plot
   portfolio-tools composition -f portfolio.json

   # Using a specific portfolio file
   portfolio-tools composition -f tests/examples/basic_portfolio.json

Example output: Opens a matplotlib window showing portfolio composition as a pie chart.

Portfolio Evolution
~~~~~~~~~~~~~~~~~~~

Plot the evolution of your portfolio value over time:

.. code-block:: bash

   # Plot portfolio evolution
   portfolio-tools plot-portfolio -f portfolio.json

   # With example file
   portfolio-tools plot-portfolio -f tests/examples/multi_currency_portfolio.json

Current Positions
~~~~~~~~~~~~~~~~~

Display current portfolio positions in a formatted table:

.. code-block:: bash

   # Show current positions
   portfolio-tools print-positions -f portfolio.json

   # Show positions for a specific date
   portfolio-tools print-positions -f portfolio.json -d 2025-06-15

Example output:

.. code-block:: text

   Current positions as of 2025-07-17:
   | Ticker  | Price Base  | Cost        | Quantity  | Value Base  | Return (%)  |
   |---------|-------------|-------------|-----------|-------------|-------------|
   | AAPL    | 181.06      | 500.25      | 5.00      | 905.29      | 80.97       |
   | __EUR   | 1.00        | 499.75      | 499.75    | 499.75      | 0.00        |
   |---------|-------------|-------------|-----------|-------------|-------------|
   | TOTAL   |             | 1000.00     |           | 1405.04     | 40.50       |

Export and Debugging Commands
-----------------------------

Export Transactions
~~~~~~~~~~~~~~~~~~~

Export all portfolio transactions in CSV format:

.. code-block:: bash

   # Export transactions
   portfolio-tools export-transactions -f portfolio.json

Example output:

.. code-block:: text

   Date,Ticker,Type,Quantity,Price,Currency
   2023-01-15,AAPL,buy,10,150.25,USD
   2023-02-01,__EUR,deposit,500.00,1.00,EUR
   2023-03-15,AAPL,sell,2,160.50,USD

Debug DataFrame
~~~~~~~~~~~~~~~

Dump the internal DataFrame for debugging purposes:

.. code-block:: bash

   # Dump portfolio DataFrame
   portfolio-tools dump-data-frame -f portfolio.json

Market Data Commands
--------------------

Individual Asset Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~

Plot price evolution of specific assets:

.. code-block:: bash

   # Plot single asset in USD
   portfolio-tools plot AAPL USD

   # Plot multiple assets in EUR
   portfolio-tools plot AAPL,MSFT,GOOGL EUR

   # Plot with different currency
   portfolio-tools plot SHOP,RY.TO CAD

Asset Correlation Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculate correlation between multiple assets:

.. code-block:: bash

   # Basic correlation analysis
   portfolio-tools correlation -t AAPL,MSFT,GOOGL

   # Correlation with international stocks
   portfolio-tools correlation -t AAPL,ASML,TSM

Example output:

.. code-block:: text

   |-------------------------------------|
   | Ticker 1  | Ticker 2  | Correlation |
   |-----------|-----------|-------------|
   | AAPL      | MSFT      | 0.7521      |
   | AAPL      | GOOGL     | 0.6834      |
   | MSFT      | GOOGL     | 0.8102      |
   |-------------------------------------|

Ticker Information
~~~~~~~~~~~~~~~~~~

Get detailed information about specific tickers:

.. code-block:: bash

   # Basic ticker information
   portfolio-tools ticker-info AAPL

   # International ticker
   portfolio-tools ticker-info ASML

Example output:

.. code-block:: text

   📊 Ticker Information: AAPL
   ==================================================
   💰 Currency: USD

   🏢 Company Name        : Apple Inc.
   🏭 Sector             : Technology
   🔧 Industry           : Consumer Electronics
   🌍 Country            : United States
   💹 Market Cap         : $3.2T
   💵 Current Price      : 208.62 USD
   📉 Previous Close     : 207.15 USD
   📊 Beta               : 1.25
   📈 P/E Ratio          : 32.4
   💰 Dividend Yield     : 0.45%
   📉 52W Low            : 164.08 USD
   📈 52W High           : 237.23 USD

   ✅ Information retrieved and cached for AAPL

Currency Conversion
~~~~~~~~~~~~~~~~~~~

Convert ticker prices between currencies:

.. code-block:: bash

   # Convert AAPL prices to EUR (default 5 days)
   portfolio-tools convert-currency AAPL EUR

   # Show more historical days
   portfolio-tools convert-currency AAPL EUR --days 10

   # Convert Canadian stock to USD
   portfolio-tools convert-currency SHOP USD --days 3

Example output:

.. code-block:: text

   💱 Converting AAPL prices to EUR
   ==================================================
   📊 Original currency: USD

   📈 Recent 5 days of price data:
                Original (USD)  Converted (EUR)
   2025-07-11         205.12         186.45
   2025-07-12         207.85         188.93
   2025-07-15         208.21         189.26
   2025-07-16         209.44         190.38
   2025-07-17         208.62         189.63

   📊 Summary Statistics:
   Latest price (USD): 208.62
   Latest price (EUR): 189.63
   Daily change: -0.39%

   ✅ Successfully converted AAPL from USD to EUR

Utility Commands
----------------

Cache Management
~~~~~~~~~~~~~~~~

Clear cached data to force fresh downloads:

.. code-block:: bash

   # Clear all cache files
   portfolio-tools clear-cache

Example output:

.. code-block:: text

   Found 9 cache files to delete:
     - 4 historical data files
     - 5 ticker info files

   Deleted: 20250717-AAPL_historical_data.pkl
   Deleted: 20250717-CADEUR=X_historical_data.pkl
   Deleted: 20250717-USDEUR=X_historical_data.pkl
   Deleted: 20250717-SHOP_historical_data.pkl
   Deleted: 20250717-AAPL_info.pkl

   ✅ Successfully cleared 9 cache files.

Development and Local Usage
---------------------------

For development purposes, you can also run commands using the module directly:

.. code-block:: bash

   # Using module directly
   python -m cli.cli --help
   python -m cli.cli composition -f portfolio.json
   python -m cli.cli ticker-info AAPL

Common Workflows
----------------

Portfolio Analysis Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Complete workflow for analyzing a portfolio:

.. code-block:: bash

   # 1. Check portfolio positions
   portfolio-tools print-positions -f my_portfolio.json

   # 2. Analyze composition
   portfolio-tools composition -f my_portfolio.json

   # 3. Check portfolio evolution
   portfolio-tools plot-portfolio -f my_portfolio.json

   # 4. Export data for external analysis
   portfolio-tools export-transactions -f my_portfolio.json > transactions.csv

Market Research Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~

Research workflow for new investments:

.. code-block:: bash

   # 1. Get detailed ticker information
   portfolio-tools ticker-info NVDA

   # 2. Check price evolution in your preferred currency
   portfolio-tools plot NVDA EUR

   # 3. Compare with similar stocks
   portfolio-tools correlation -t NVDA,AMD,INTC

   # 4. Convert prices to your base currency
   portfolio-tools convert-currency NVDA EUR --days 30

Error Handling
--------------

The CLI provides helpful error messages for common issues:

File Not Found
~~~~~~~~~~~~~~

.. code-block:: bash

   $ portfolio-tools composition -f nonexistent.json
   Error: Portfolio file 'nonexistent.json' not found.

Invalid Ticker
~~~~~~~~~~~~~~

.. code-block:: bash

   $ portfolio-tools ticker-info INVALID
   ❌ Error getting ticker information: No data found for ticker INVALID

Missing Arguments
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ portfolio-tools plot
   Usage: portfolio-tools plot [OPTIONS] TICKERS CURRENCY
   Try 'portfolio-tools plot --help' for help.

   Error: Missing argument 'TICKERS'.

Network Issues
~~~~~~~~~~~~~~

.. code-block:: bash

   $ portfolio-tools ticker-info AAPL
   ❌ Error getting ticker information: HTTPSConnectionPool(...): Max retries exceeded

Best Practices
--------------

1. **Use absolute paths** for portfolio files when running from different directories:

   .. code-block:: bash

      portfolio-tools composition -f /path/to/portfolio.json

2. **Clear cache periodically** to ensure fresh data:

   .. code-block:: bash

      portfolio-tools clear-cache

3. **Use specific dates** for historical analysis:

   .. code-block:: bash

      portfolio-tools print-positions -f portfolio.json -d 2025-06-30

4. **Combine commands** for comprehensive analysis:

   .. code-block:: bash

      # Analysis script
      portfolio-tools clear-cache
      portfolio-tools print-positions -f portfolio.json
      portfolio-tools composition -f portfolio.json
      portfolio-tools plot-portfolio -f portfolio.json

5. **Export data** for further analysis in other tools:

   .. code-block:: bash

      portfolio-tools export-transactions -f portfolio.json > analysis/transactions.csv

Command Reference Quick Card
----------------------------

.. code-block:: text

   Portfolio Commands:
   ├── composition          Plot portfolio composition
   ├── plot-portfolio       Plot portfolio evolution  
   ├── print-positions      Show current positions
   ├── export-transactions  Export transactions to CSV
   └── dump-data-frame     Debug portfolio DataFrame

   Market Data Commands:
   ├── plot                Plot asset price evolution
   ├── correlation         Calculate asset correlations
   ├── ticker-info         Show detailed ticker info
   └── convert-currency    Convert prices between currencies

   Utility Commands:
   ├── clear-cache         Clear cached data
   ├── --help             Show help information
   └── --version          Show version

Getting Help
------------

For more help with any command:

.. code-block:: bash

   # General help
   portfolio-tools --help

   # Command-specific help
   portfolio-tools <command> --help

   # Example
   portfolio-tools ticker-info --help
