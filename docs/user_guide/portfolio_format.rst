Portfolio JSON Format
====================

Portfolio Toolkit uses a structured JSON format (Version 2) for storing portfolio data. This format supports multi-currency transactions, FIFO cost tracking, and comprehensive transaction history.

JSON Structure Overview
----------------------

The portfolio JSON file has four main sections:

1. **Portfolio Metadata**: Basic information about the portfolio
2. **Transactions**: Flat array of all transactions (deposits, withdrawals, buys, sells)
3. **Splits**: Array of stock split events (optional)

Basic Structure
--------------

.. code-block:: json

   {
     "name": "Portfolio Name",
     "currency": "EUR",
     "transactions": [
       // Array of transaction objects
     ],
     "splits": [
       // Array of stock split objects (optional)
     ]
   }

Portfolio Metadata Fields
-------------------------

name
~~~~
- **Type**: String
- **Required**: Yes
- **Description**: Display name for the portfolio
- **Example**: ``"My Investment Portfolio"``

currency
~~~~~~~~
- **Type**: String
- **Required**: Yes
- **Description**: Base currency for the portfolio (ISO 4217 code)
- **Supported**: EUR, USD, CAD, GBP, etc.
- **Example**: ``"EUR"``

Transaction Structure
--------------------

Each transaction in the ``transactions`` array must include the following fields:

Core Fields
~~~~~~~~~~~

ticker
^^^^^^
- **Type**: String or null
- **Required**: Yes
- **Description**: Asset symbol (e.g., "AAPL") or ``null`` for cash transactions
- **Examples**: ``"AAPL"``, ``"GOOGL"``, ``null``

date
^^^^
- **Type**: String
- **Required**: Yes
- **Format**: YYYY-MM-DD
- **Description**: Transaction date
- **Example**: ``"2025-06-12"``

type
^^^^
- **Type**: String
- **Required**: Yes
- **Values**: ``"buy"``, ``"sell"``, ``"deposit"``, ``"withdrawal"``
- **Description**: Type of transaction

quantity
^^^^^^^^
- **Type**: Number
- **Required**: Yes
- **Description**: Number of shares (stocks) or amount (cash)
- **Example**: ``10`` (shares), ``1000.00`` (cash amount)

price
^^^^^
- **Type**: Number
- **Required**: Yes
- **Description**: Price per share (stocks) or ``1.00`` (cash)
- **Example**: ``150.25`` (stock price), ``1.00`` (cash)

Currency and Conversion Fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

currency
^^^^^^^^
- **Type**: String
- **Required**: Yes
- **Description**: Currency of the transaction
- **Example**: ``"USD"``, ``"EUR"``, ``"CAD"``

total
^^^^^
- **Type**: Number
- **Required**: Yes
- **Description**: Total amount in transaction currency
- **Calculation**: ``quantity × price``
- **Example**: ``1500.00``

exchange_rate
^^^^^^^^^^^^^
- **Type**: Number
- **Required**: Yes
- **Description**: Exchange rate from transaction currency to base currency
- **Format**: How many units of transaction currency per 1 unit of base currency
- **Example**: ``1.056`` (EUR/USD rate)

subtotal_base
^^^^^^^^^^^^^
- **Type**: Number
- **Required**: Yes
- **Description**: Transaction amount in base currency before fees
- **Calculation**: ``total ÷ exchange_rate``
- **Example**: ``1420.45``

fees_base
^^^^^^^^^
- **Type**: Number
- **Required**: Yes
- **Description**: Transaction fees in base currency
- **Example**: ``2.50``

total_base
^^^^^^^^^^
- **Type**: Number
- **Required**: Yes
- **Description**: Total cost in base currency including fees
- **Calculation**: ``subtotal_base + fees_base`` (buy) or ``subtotal_base - fees_base`` (sell)
- **Example**: ``1422.95``

Transaction Types
----------------

Stock Purchase (Buy)
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "ticker": "AAPL",
     "date": "2025-06-12",
     "type": "buy",
     "quantity": 10,
     "price": 150.00,
     "currency": "USD",
     "total": 1500.00,
     "exchange_rate": 1.056,
     "subtotal_base": 1420.45,
     "fees_base": 2.50,
     "total_base": 1422.95
   }

Stock Sale (Sell)
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "ticker": "AAPL",
     "date": "2025-06-15",
     "type": "sell",
     "quantity": 5,
     "price": 155.00,
     "currency": "USD",
     "total": 775.00,
     "exchange_rate": 1.058,
     "subtotal_base": 732.58,
     "fees_base": 2.00,
     "total_base": 730.58
   }

Cash Deposit
~~~~~~~~~~~

.. code-block:: json

   {
     "ticker": null,
     "date": "2025-06-10",
     "type": "deposit",
     "quantity": 1000.00,
     "price": 1.00,
     "currency": "EUR",
     "total": 1000.00,
     "exchange_rate": 1.00,
     "subtotal_base": 1000.00,
     "fees_base": 0.00,
     "total_base": 1000.00
   }

Cash Withdrawal
~~~~~~~~~~~~~~

.. code-block:: json

   {
     "ticker": null,
     "date": "2025-06-20",
     "type": "withdrawal",
     "quantity": 500.00,
     "price": 1.00,
     "currency": "EUR",
     "total": 500.00,
     "exchange_rate": 1.00,
     "subtotal_base": 500.00,
     "fees_base": 5.00,
     "total_base": 505.00
   }

Stock Splits Structure
---------------------

The ``splits`` array is optional and contains stock split events that automatically adjust historical positions. Each split object includes the following fields:

Split Fields
~~~~~~~~~~~

ticker
^^^^^^
- **Type**: String
- **Required**: Yes
- **Description**: Stock symbol that underwent the split
- **Example**: ``"EVTL"``, ``"AAPL"``, ``"GOOGL"``

date
^^^^
- **Type**: String
- **Required**: Yes
- **Format**: YYYY-MM-DD
- **Description**: Date when the stock split became effective
- **Example**: ``"2024-09-23"``

ratio
^^^^^
- **Type**: String
- **Required**: Yes
- **Description**: Human-readable split ratio
- **Format**: ``"new:old"`` (e.g., "2:1" for a 2-for-1 split)
- **Examples**: ``"2:1"`` (split), ``"4:1"`` (split), ``"1:10"`` (reverse split)

split_factor
^^^^^^^^^^^^
- **Type**: Number
- **Required**: Yes
- **Description**: Numerical factor to multiply existing shares
- **Calculation**: ``new_shares = old_shares × split_factor``
- **Examples**: ``2.0`` (2:1 split), ``0.1`` (1:10 reverse split)

Split Types
~~~~~~~~~~

Forward Stock Split (2:1)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: json

   {
     "ticker": "AAPL",
     "date": "2024-08-31",
     "ratio": "4:1",
     "split_factor": 4.0
   }

**Effect**: 100 shares become 400 shares, price adjusts from $200 to $50

Reverse Stock Split (1:10)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: json

   {
     "ticker": "EVTL",
     "date": "2024-09-23",
     "ratio": "1:10",
     "split_factor": 0.1
   }

**Effect**: 1000 shares become 100 shares, price adjusts from $1 to $10

Split Processing
~~~~~~~~~~~~~~~

When a split is processed:

1. **Automatic Adjustment**: All positions held before the split date are automatically adjusted
2. **FIFO Preservation**: The system maintains FIFO cost basis tracking
3. **Fractional Shares**: For reverse splits, fractional shares are converted to cash
4. **Transaction Creation**: The system creates sell/buy transactions to represent the split

.. note::
   Splits are processed automatically when loading the portfolio. The original transactions remain unchanged, but the effective position calculations account for all splits.

Complete Split Example
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "splits": [
       {
         "ticker": "AAPL",
         "date": "2022-08-31",
         "ratio": "4:1",
         "split_factor": 4.0
       },
       {
         "ticker": "EVTL",
         "date": "2024-09-23",
         "ratio": "1:10",
         "split_factor": 0.1
       }
     ]
   }

Complete Example
---------------

Here's a complete portfolio JSON file with splits:

.. code-block:: json

   {
     "name": "Sample Multi-Currency Portfolio",
     "currency": "EUR",
     "transactions": [
       {
         "ticker": null,
         "date": "2025-06-01",
         "type": "deposit",
         "quantity": 5000.00,
         "price": 1.00,
         "currency": "EUR",
         "total": 5000.00,
         "exchange_rate": 1.00,
         "subtotal_base": 5000.00,
         "fees_base": 0.00,
         "total_base": 5000.00
       },
       {
         "ticker": "AAPL",
         "date": "2025-06-05",
         "type": "buy",
         "quantity": 20,
         "price": 150.00,
         "currency": "USD",
         "total": 3000.00,
         "exchange_rate": 1.056,
         "subtotal_base": 2840.91,
         "fees_base": 5.00,
         "total_base": 2845.91
       },
       {
         "ticker": "SHOP",
         "date": "2025-06-08",
         "type": "buy",
         "quantity": 15,
         "price": 80.00,
         "currency": "CAD",
         "total": 1200.00,
         "exchange_rate": 0.639,
         "subtotal_base": 766.82,
         "fees_base": 8.18,
         "total_base": 775.00
       },
       {
         "ticker": "AAPL",
         "date": "2025-06-12",
         "type": "sell",
         "quantity": 5,
         "price": 160.00,
         "currency": "USD",
         "total": 800.00,
         "exchange_rate": 1.058,
         "subtotal_base": 756.33,
         "fees_base": 3.00,
         "total_base": 753.33
       }
     ],
     "splits": [
       {
         "ticker": "AAPL",
         "date": "2024-08-31",
         "ratio": "4:1",
         "split_factor": 4.0
       },
       {
         "ticker": "EVTL",
         "date": "2024-09-23",
         "ratio": "1:10",
         "split_factor": 0.1
       }
     ]
   }

Validation Rules
---------------

The following validation rules apply:

Required Fields
~~~~~~~~~~~~~~
- All transaction fields listed above are required
- No field can be null except ``ticker`` for cash transactions
- Split fields are required when ``splits`` array is present

Data Types
~~~~~~~~~
- Dates must be in YYYY-MM-DD format
- Numbers must be positive (except split_factor which can be any positive number)
- Strings must not be empty
- Split ratios must follow "new:old" format

Logical Consistency
~~~~~~~~~~~~~~~~~
- Cash transactions (``ticker: null``) must have ``price: 1.00``
- ``total`` must equal ``quantity × price``
- Exchange rates must be positive
- For base currency transactions, ``exchange_rate`` should be ``1.00``
- Split dates must be valid dates
- Split factors must be positive numbers
- Split ratios must match the split_factor calculation

Split-Specific Rules
~~~~~~~~~~~~~~~~~~
- Split dates should be before any dependent transactions
- Split factors must be consistent with ratios (e.g., "2:1" → 2.0, "1:10" → 0.1)
- Tickers in splits must correspond to actual stock transactions
- Multiple splits for the same ticker must be in chronological order

Common Mistakes
--------------

Incorrect Exchange Rate Direction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   // ❌ Wrong: Using USD/EUR instead of EUR/USD
   {
     "currency": "USD",
     "exchange_rate": 0.946  // This is USD/EUR, not EUR/USD
   }

   // ✅ Correct: Using EUR/USD
   {
     "currency": "USD",
     "exchange_rate": 1.056  // This is EUR/USD
   }

Missing Fee Conversion
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   // ❌ Wrong: Fees in transaction currency
   {
     "currency": "USD",
     "fees_base": 2.50  // Should be converted to base currency
   }

   // ✅ Correct: Fees in base currency
   {
     "currency": "USD",
     "exchange_rate": 1.056,
     "fees_base": 2.37  // 2.50 USD ÷ 1.056 = 2.37 EUR
   }

Inconsistent Totals
~~~~~~~~~~~~~~~~~~

.. code-block:: json

   // ❌ Wrong: total_base doesn't include fees
   {
     "subtotal_base": 1000.00,
     "fees_base": 5.00,
     "total_base": 1000.00  // Should be 1005.00 for buy
   }

   // ✅ Correct: total_base includes fees
   {
     "subtotal_base": 1000.00,
     "fees_base": 5.00,
     "total_base": 1005.00  // For buy transactions
   }

Incorrect Split Factor
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   // ❌ Wrong: Split factor doesn't match ratio
   {
     "ticker": "AAPL",
     "ratio": "2:1",
     "split_factor": 0.5  // Should be 2.0 for a 2:1 split
   }

   // ✅ Correct: Split factor matches ratio
   {
     "ticker": "AAPL",
     "ratio": "2:1",
     "split_factor": 2.0  // 2 new shares for 1 old share
   }

   // ✅ Correct: Reverse split
   {
     "ticker": "EVTL",
     "ratio": "1:10",
     "split_factor": 0.1  // 1 new share for 10 old shares
   }

Best Practices
-------------

1. **Consistent Currency Codes**: Use ISO 4217 currency codes (EUR, USD, CAD)
2. **Accurate Exchange Rates**: Use exchange rates from the actual transaction date
3. **Include All Fees**: Account for all transaction costs in ``fees_base``
4. **Chronological Order**: Sort transactions by date for easier debugging
5. **Validation**: Use the validation script to check your portfolio format

Tools and Utilities
------------------

Portfolio Toolkit provides several utilities for working with JSON files:

.. code-block:: bash

   # Validate portfolio format
   python tests/validate_examples.py

   # Parse and validate portfolio using CLI
   portfolio-toolkit portfolio parse examples/portfolio_example.json

   # Display portfolio summary with current positions
   portfolio-toolkit portfolio summary examples/portfolio_example.json

   # Show portfolio performance analysis
   portfolio-toolkit portfolio performance examples/portfolio_example.json

   # Convert portfolio to different formats
   portfolio-toolkit portfolio export examples/portfolio_example.json --format csv

You can also use the CLI to work with portfolio data interactively:

.. code-block:: bash

   # Show all available portfolio commands
   portfolio-toolkit portfolio --help

   # Validate portfolio format and check for errors
   portfolio-toolkit portfolio validate examples/portfolio_example.json

   # Display detailed transaction history
   portfolio-toolkit portfolio transactions examples/portfolio_example.json

For more information about CLI commands, see the :doc:`CLI Reference <../cli_reference>`.
