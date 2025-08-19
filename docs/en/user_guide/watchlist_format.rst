Watchlist JSON Format
=====================

Portfolio Toolkit uses a structured JSON format for storing asset watchlists. This format is much simpler than the Portfolio format and is designed to facilitate asset tracking and monitoring.

JSON Structure Overview
-----------------------

The Watchlist JSON file has two main sections:

1. **Watchlist Metadata**: Basic information about the asset list
2. **Assets**: An array of objects representing the assets to track

Basic Structure
---------------

.. code-block:: json

   {
     "name": "Watchlist Name",
     "currency": "USD",
     "assets": [
       { "ticker": "AAPL" },
       { "ticker": "GOOGL" },
       { "ticker": "MSFT" }
     ]
   }

Watchlist Metadata Fields
--------------------------

name
~~~~
- **Type**: String
- **Required**: Yes
- **Description**: Display name for the watchlist
- **Example**: ``"Tech Stocks Watchlist"``

currency
~~~~~~~~
- **Type**: String
- **Required**: Yes
- **Description**: Base currency for the watchlist (ISO 4217 code)
- **Supported**: USD, EUR, CAD, GBP, etc.
- **Example**: ``"USD"``

Assets Structure
----------------

Each object in the ``assets`` array must include the following field:

ticker
^^^^^^
- **Type**: String
- **Required**: Yes
- **Description**: Asset symbol (e.g., "AAPL", "GOOGL")
- **Example**: ``"AAPL"``

Complete Example
----------------

Here's a complete example of a Watchlist JSON file:

.. code-block:: json

   {
     "name": "Tech Stocks Watchlist",
     "currency": "USD",
     "assets": [
       { "ticker": "AAPL" },
       { "ticker": "GOOGL" },
       { "ticker": "MSFT" },
       { "ticker": "AMZN" }
     ]
   }

Validation Rules
----------------

The following validation rules apply:

Required Fields
~~~~~~~~~~~~~~~
- All fields listed above are required
- No field can be ``null``

Data Types
~~~~~~~~~~
- ``name`` and ``currency`` must be non-empty strings
- ``ticker`` must be a valid string

Logical Consistency
~~~~~~~~~~~~~~~~~~~
- ``currency`` must be a valid ISO 4217 code
- ``ticker`` values must be unique within the watchlist

Best Practices
--------------

1. **Consistent Currency Codes**: Use ISO 4217 currency codes (USD, EUR, CAD)
2. **Unique Tickers**: Avoid duplicates in the asset list
3. **Validation**: Use validation tools to check your watchlist format
4. **Meaningful Names**: Choose descriptive names for your watchlists
5. **Logical Grouping**: Group related assets together (e.g., by sector, region)

Tools and Utilities
-------------------

Portfolio Toolkit provides utilities for working with Watchlist JSON files:

.. code-block:: bash

   # Validate watchlist format
   python -m portfolio_toolkit.watchlist.validate

   # Print watchlist information using CLI
   python -m cli.cli watchlist print -f my_watchlist.json

Common Use Cases
---------------

**Sector-Based Watchlist**

.. code-block:: json

   {
     "name": "Technology Sector ETFs",
     "currency": "USD",
     "assets": [
       { "ticker": "QQQ" },
       { "ticker": "VGT" },
       { "ticker": "XLK" },
       { "ticker": "FTEC" }
     ]
   }

**International Markets Watchlist**

.. code-block:: json

   {
     "name": "Global Market Tracking",
     "currency": "EUR",
     "assets": [
       { "ticker": "VTI" },
       { "ticker": "VXUS" },
       { "ticker": "VEA" },
       { "ticker": "VWO" }
     ]
   }

**Individual Stocks Watchlist**

.. code-block:: json

   {
     "name": "Blue Chip Stocks",
     "currency": "USD",
     "assets": [
       { "ticker": "AAPL" },
       { "ticker": "MSFT" },
       { "ticker": "GOOGL" },
       { "ticker": "AMZN" },
       { "ticker": "TSLA" }
     ]
   }