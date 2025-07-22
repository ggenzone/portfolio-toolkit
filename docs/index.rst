Portfolio Tools Documentation
==============================

.. image:: https://img.shields.io/badge/python-3.8%2B-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/github/license/ggenzone/portfolio-tools.svg
   :target: https://github.com/ggenzone/portfolio-tools/blob/main/LICENSE
   :alt: License

.. image:: https://img.shields.io/badge/docs-sphinx-brightgreen.svg
   :target: https://ggenzone.github.io/portfolio-tools/
   :alt: Documentation

Portfolio Tools is a comprehensive Python library for portfolio management, analysis, and visualization. It supports multi-currency portfolios with automatic currency conversion, FIFO cost calculation, and advanced analytics.

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

   git clone https://github.com/ggenzone/portfolio-tools.git
   cd portfolio-tools
   pip install -r requirements.txt

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from portfolio_tools.portfolio.portfolio import Portfolio
   from portfolio_tools.data_provider.yf_data_provider import YFDataProvider

   # Create a data provider
   data_provider = YFDataProvider()

   # Load portfolio from JSON
   portfolio = Portfolio('path/to/portfolio.json', data_provider)

   # Print current positions
   portfolio.print_current_positions()

   # Plot portfolio composition
   portfolio.plot_composition()

Portfolio JSON Format
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "name": "My Portfolio",
     "currency": "EUR",
     "transactions": [
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
       }
     ]
   }

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Print current positions
   python -m cli.cli print-positions portfolio.json

   # Export transactions to CSV
   python -m cli.cli export-transactions portfolio.json

   # Plot portfolio composition
   python -m cli.cli plot portfolio.json

API Reference
-------------

.. toctree::
   :maxdepth: 2
   :caption: API Documentation

   api/portfolio_tools
   api/modules

Examples
--------

.. toctree::
   :maxdepth: 2
   :caption: Examples

   examples/basic_usage
   examples/cli_usage
   examples/multi_currency
   examples/advanced_analysis

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
   user_guide/migration


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
