Optimization JSON Format
========================

Portfolio Toolkit uses a structured JSON format for storing portfolio optimization data. This format is similar to the Watchlist format, but allows including quantities (`quantity`) for each asset, which facilitates analysis and optimization.

JSON Structure Overview
-----------------------

The Optimization JSON file has two main sections:

1. **Optimization Metadata**: Basic information about the optimization
2. **Assets**: An array of objects representing the assets, with optional quantities

Basic Structure
---------------

.. code-block:: json

   {
     "name": "Optimization Name",
     "currency": "USD",
     "assets": [
       { "ticker": "AAPL", "quantity": 50 },
       { "ticker": "GOOGL" },
       { "ticker": "MSFT", "quantity": 30 }
     ]
   }

Optimization Metadata Fields
-----------------------------

name
~~~~
- **Type**: String
- **Required**: Yes
- **Description**: Display name for the optimization
- **Example**: ``"Tech Portfolio Optimization"``

currency
~~~~~~~~
- **Type**: String
- **Required**: Yes
- **Description**: Base currency for the optimization (ISO 4217 code)
- **Supported**: USD, EUR, CAD, GBP, etc.
- **Example**: ``"USD"``

Assets Structure
----------------

Each object in the ``assets`` array can include the following fields:

ticker
^^^^^^
- **Type**: String
- **Required**: Yes
- **Description**: Asset symbol (e.g., "AAPL", "GOOGL")
- **Example**: ``"AAPL"``

quantity
^^^^^^^^
- **Type**: Float
- **Required**: No
- **Description**: Quantity of the asset for analysis and optimization
- **Example**: ``50.0``

Complete Example
----------------

Here's a complete example of an Optimization JSON file:

.. code-block:: json

   {
     "name": "Tech Portfolio Optimization",
     "currency": "USD",
     "assets": [
       { "ticker": "AAPL", "quantity": 50.0 },
       { "ticker": "GOOGL" },
       { "ticker": "MSFT", "quantity": 30.0 },
       { "ticker": "AMZN", "quantity": 25.0 },
       { "ticker": "TSLA" }
     ]
   }

Validation Rules
----------------

The following validation rules apply:

Required Fields
~~~~~~~~~~~~~~~
- All fields listed above are required, except `quantity`
- No required field can be ``null``

Data Types
~~~~~~~~~~
- ``name`` and ``currency`` must be non-empty strings
- ``ticker`` must be a valid string
- ``quantity`` must be a positive float if present

Logical Consistency
~~~~~~~~~~~~~~~~~~~
- ``currency`` must be a valid ISO 4217 code
- ``ticker`` values must be unique within the asset list
- ``quantity`` values should be positive when specified

Best Practices
--------------

1. **Consistent Currency Codes**: Use ISO 4217 currency codes (USD, EUR, CAD)
2. **Unique Tickers**: Avoid duplicates in the asset list
3. **Optional Quantities**: Include `quantity` only when relevant for analysis
4. **Meaningful Names**: Choose descriptive names for your optimizations
5. **Logical Grouping**: Group related assets for better optimization results
6. **Data Validation**: Validate your optimization file before running analysis

Tools and Utilities
-------------------

Portfolio Toolkit provides utilities for working with Optimization JSON files:

.. code-block:: bash

   # Validate optimization format
   python -m portfolio_toolkit.optimization.validate

   # Run optimization analysis using CLI
   python -m cli.cli optimization calc -f my_optimization.json
   python -m cli.cli optimization optimize -f my_optimization.json
   python -m cli.cli optimization plot -f my_optimization.json

Common Use Cases
---------------

**Equal-Weight Portfolio Optimization**

.. code-block:: json

   {
     "name": "Equal Weight Tech Portfolio",
     "currency": "USD",
     "assets": [
       { "ticker": "AAPL", "quantity": 100.0 },
       { "ticker": "MSFT", "quantity": 100.0 },
       { "ticker": "GOOGL", "quantity": 100.0 },
       { "ticker": "AMZN", "quantity": 100.0 }
     ]
   }

**Market Cap Weighted Portfolio**

.. code-block:: json

   {
     "name": "Market Cap Weighted Portfolio",
     "currency": "USD", 
     "assets": [
       { "ticker": "AAPL", "quantity": 200.0 },
       { "ticker": "MSFT", "quantity": 150.0 },
       { "ticker": "GOOGL", "quantity": 100.0 },
       { "ticker": "AMZN", "quantity": 80.0 },
       { "ticker": "TSLA", "quantity": 50.0 }
     ]
   }

**Asset Allocation Study**

.. code-block:: json

   {
     "name": "60/40 Portfolio Optimization",
     "currency": "USD",
     "assets": [
       { "ticker": "VTI", "quantity": 600.0 },
       { "ticker": "BND", "quantity": 400.0 }
     ]
   }

**Sector Diversification**

.. code-block:: json

   {
     "name": "Sector Diversified Portfolio",
     "currency": "USD",
     "assets": [
       { "ticker": "XLK", "quantity": 50.0 },
       { "ticker": "XLF", "quantity": 50.0 },
       { "ticker": "XLV", "quantity": 50.0 },
       { "ticker": "XLE", "quantity": 50.0 },
       { "ticker": "XLI", "quantity": 50.0 }
     ]
   }

Optimization Parameters
----------------------

While not part of the JSON format, optimization analysis considers:

**Risk Metrics**
- Volatility (standard deviation)
- Value at Risk (VaR)
- Maximum drawdown
- Beta relative to benchmark

**Return Metrics**
- Expected returns
- Sharpe ratio
- Sortino ratio
- Alpha generation

**Correlation Analysis**
- Asset correlation matrix
- Diversification benefits
- Risk concentration