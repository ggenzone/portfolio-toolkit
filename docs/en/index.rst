Portfolio Tools Documentation
==============================

.. raw:: html

   <div style="background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 6px; padding: 16px; margin-bottom: 24px; text-align: center;">
      <span style="margin-right: 12px;">🌐</span>
      <strong>Language / Idioma:</strong>
      <span style="margin: 0 8px;">English (current)</span>
      <a href="./es/" style="color: #0366d6; text-decoration: none; font-weight: 500;">Español</a>
   </div>

.. image:: https://img.shields.io/badge/python-3.9%2B-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/github/license/ggenzone/portfolio-toolkit.svg
   :target: https://github.com/ggenzone/portfolio-toolkit/blob/main/LICENSE
   :alt: License

.. image:: https://img.shields.io/badge/docs-sphinx-brightgreen.svg
   :target: https://ggenzone.github.io/portfolio-toolkit/
   :alt: Documentation

Portfolio Toolkit is a comprehensive Python library for portfolio management, analysis, and visualization. It supports multi-currency portfolios with automatic currency conversion, FIFO cost calculation, and advanced analytics.

Features
--------

* **Multi-Currency Support**: Handle portfolios with transactions in different currencies (USD, EUR, CAD, etc.)
* **FIFO Cost Calculation**: Accurate cost basis tracking using First-In-First-Out methodology
* **Automatic Currency Conversion**: Real-time currency conversion with configurable exchange rates
* **Portfolio Analytics**: Comprehensive analysis tools including returns, composition, and evolution tracking
* **Data Visualization**: Rich plotting capabilities for portfolio composition and performance analysis
* **CSV Export**: Export transaction data and portfolio positions to CSV format
* **CLI Interface**: Powerful command-line tools built with Click for portfolio analysis, data visualization, and market research

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install portfolio-toolkit

Basic Usage (CLI)
~~~~~~~~~~~~~~~~~

The easiest way to get started is using the command-line interface:

.. code-block:: bash

   # View available commands
   portfolio-toolkit --help

   # Show current portfolio positions
   portfolio-toolkit portfolio positions portfolio.json 2025-07-30

   # View portfolio transactions
   portfolio-toolkit portfolio transactions portfolio.json

   # Analyze performance over time
   portfolio-toolkit portfolio performance portfolio.json

   # Generate portfolio evolution chart
   portfolio-toolkit portfolio evolution portfolio.json

Library Usage
~~~~~~~~~~~~~

For programmatic access, you can use the Python library:

.. code-block:: python

   from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
   from portfolio_toolkit.portfolio.load_portfolio_json import load_portfolio_json
   from portfolio_toolkit.cli.commands.utils import load_json_file

   # Load portfolio
   data = load_json_file('portfolio.json')
   data_provider = YFDataProvider()
   portfolio = load_portfolio_json(data, data_provider=data_provider)

For detailed library usage, see :doc:`examples/basic_usage`.

Portfolio JSON Format
~~~~~~~~~~~~~~~~~~~~

Create a portfolio JSON file to get started. For detailed format documentation, see :doc:`user_guide/portfolio_format`.

.. code-block:: json

   {
     "name": "My Investment Portfolio",
     "currency": "USD",
     "account": [
       {
         "date": "2023-01-15",
         "type": "deposit",
         "amount": 10000,
         "currency": "USD"
       }
     ],
     "assets": [
       {
         "ticker": "AAPL",
         "transactions": [
           {
             "date": "2023-01-20", 
             "type": "buy",
             "quantity": 50,
             "price": 150.25,
             "currency": "USD"
           }
         ]
       },
       {
         "ticker": "MSFT",
         "transactions": [
           {
             "date": "2023-02-10",
             "type": "buy", 
             "quantity": 30,
             "price": 280.50,
             "currency": "USD"
           }
         ]
       }
     ]
   }

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

The CLI provides powerful tools for portfolio analysis:

.. code-block:: bash

   # Portfolio analysis commands
   portfolio-toolkit portfolio transactions portfolio.json              # View transactions
   portfolio-toolkit portfolio positions portfolio.json 2025-07-30     # Current positions
   portfolio-toolkit portfolio performance portfolio.json               # Performance analysis
   portfolio-toolkit portfolio evolution portfolio.json                 # Evolution chart

   # Export options
   portfolio-toolkit portfolio transactions portfolio.json --output transactions.csv
   portfolio-toolkit portfolio performance portfolio.json --output performance.csv

   # Performance analysis with different time periods
   portfolio-toolkit portfolio performance portfolio.json --period-type months -n 6
   portfolio-toolkit portfolio performance portfolio.json --period-type quarters -n 4

For comprehensive CLI documentation, see :doc:`examples/cli_usage`.


Examples
--------

.. toctree::
   :maxdepth: 2
   :caption: Examples

   examples/cli_usage
   examples/basic_usage
   examples/multi_currency

User Guide
----------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   user_guide/installation
   user_guide/getting_started
   user_guide/watchlist_format
   user_guide/optimization_format
   user_guide/portfolio_format


API Reference
-------------

.. toctree::
   :maxdepth: 2
   :caption: API Documentation

   api/portfolio_toolkit
   api/modules

Testing
-------

.. toctree::
   :maxdepth: 2
   :caption: Testing

   testing/examples
   testing/validation

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
