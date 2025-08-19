Ejemplos de Uso de CLI
======================

Esta sección proporciona ejemplos completos de cómo usar la interfaz de línea de comandos (CLI) de Portfolio Toolkit. El CLI ha sido construido usando el framework Click para una experiencia intuitiva y amigable.

Instalación
-----------

Instala el paquete usando pip:

.. code-block:: bash

   pip install portfolio-toolkit

Después de la instalación, puedes acceder al CLI directamente:

.. code-block:: bash

   # Ver comandos disponibles
   portfolio-toolkit --help

   # Verificar versión
   portfolio-toolkit --version

Crear tu Archivo de Cartera
---------------------------

Antes de usar los comandos CLI, necesitas crear un archivo JSON de cartera que describa tus inversiones. Para información detallada sobre el formato del archivo de cartera, ve :doc:`../user_guide/portfolio_format`.

Aquí hay un ejemplo básico de un archivo de cartera:

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

Guarda esto como ``portfolio.json`` para usar con los ejemplos a continuación.

Comandos Disponibles
--------------------

El CLI está organizado alrededor de comandos de análisis de cartera. Aquí están los grupos principales de comandos y su uso:

Transacciones de Cartera
~~~~~~~~~~~~~~~~~~~~~~~~

Listar y exportar datos de transacciones desde tu cartera.

**Listar transacciones de activos:**

.. code-block:: bash

   # Mostrar todas las transacciones de activos
   portfolio-toolkit portfolio transactions portfolio.json

   # Exportar transacciones de activos a CSV
   portfolio-toolkit portfolio transactions portfolio.json --output transactions.csv

**Listar transacciones de efectivo:**

.. code-block:: bash

   # Mostrar transacciones de cuenta de efectivo (depósitos, retiros)
   portfolio-toolkit portfolio transactions portfolio.json --cash

   # Export cash transactions to CSV
   portfolio-toolkit portfolio transactions portfolio.json --cash --output cash_transactions.csv

Example output:

.. code-block:: text

   📊 Portfolio asset transactions
   ============================================================
   ticker    date        type  quantity     price currency
   AAPL   2023-01-20     buy      50.0    150.25      USD
   MSFT   2023-02-10     buy      30.0    280.50      USD

Portfolio Positions
~~~~~~~~~~~~~~~~~~~

View current portfolio positions and create visualizations.

**Show current positions:**

.. code-block:: bash

   # Show positions for a specific date
   portfolio-toolkit portfolio positions portfolio.json 2025-07-30

**Position visualizations:**

.. code-block:: bash

   # Create a pie chart of current positions
   portfolio-toolkit portfolio positions portfolio.json 2025-07-30 --plot

   # Group positions by country
   portfolio-toolkit portfolio positions portfolio.json 2025-07-30 --country

   # Group positions by sector
   portfolio-toolkit portfolio positions portfolio.json 2025-07-30 --sector

Example output:

.. code-block:: text

   📊 Portfolio Positions as of 2025-07-30
   ============================================================
   Ticker  Quantity  Current Price  Market Value  % of Portfolio
   AAPL         50         208.62      10,431.00           55.2%
   MSFT         30         445.91      13,377.30           44.8%
   ============================================================
   Total Portfolio Value: $23,808.30

Performance Analysis
~~~~~~~~~~~~~~~~~~~~

Analyze portfolio performance across different time periods.

**Basic performance analysis:**

.. code-block:: bash

   # Compare returns over the last 4 weeks (default)
   portfolio-toolkit portfolio performance portfolio.json

**Customized time periods:**

.. code-block:: bash

   # Last 4 weeks (explicit)
   portfolio-toolkit portfolio performance portfolio.json --period-type weeks -n 4

   # Last 6 months
   portfolio-toolkit portfolio performance portfolio.json --period-type months -n 6

   # Last 6 quarters
   portfolio-toolkit portfolio performance portfolio.json --period-type quarters -n 6

**Export performance data:**

.. code-block:: bash

   # Export returns to CSV file
   portfolio-toolkit portfolio performance portfolio.json --output performance.csv

**Display options:**

.. code-block:: bash

   # Show percentage returns (default)
   portfolio-toolkit portfolio performance portfolio.json --display return

   # Show absolute position values
   portfolio-toolkit portfolio performance portfolio.json --display value

Example output:

.. code-block:: text

   📊 Performance Summary - Last 4 Weeks
   ============================================================
           W27 2025    W28 2025    W29 2025    W30 2025
   AAPL    -           3.33%       2.86%       1.92%
   MSFT    -           -1.25%      4.17%       2.10%
   ============================================================
   Note: Percentage returns vs previous period

Portfolio Evolution
~~~~~~~~~~~~~~~~~~~

Visualize how your portfolio has evolved over time.

.. code-block:: bash

   # Plot portfolio evolution chart
   portfolio-toolkit portfolio evolution portfolio.json

This command creates a time-series chart showing your portfolio's value evolution, including:

- Total portfolio value over time
- Individual asset performance
- Cash position changes
- Overall return trends

Tax Reporting
~~~~~~~~~~~~~

Generate tax reports for a specific year.

.. code-block:: bash

   # Generate tax report for 2025
   portfolio-toolkit portfolio tax-report portfolio.json 2025

Example output:

.. code-block:: text

   📊 Tax Report for 2025
   ============================================================
   Realized Gains/Losses:
   
   Asset    Sale Date    Quantity  Buy Price  Sale Price  Gain/Loss
   AAPL   2025-06-15         10     150.25     180.50      +302.50
   MSFT   2025-09-20          5     280.50     275.00       -27.50
   ============================================================
   Total Realized Gain: +$275.00

Command Reference
-----------------

Complete command reference with all available options:

**portfolio transactions**

.. code-block:: text

   Usage: portfolio-toolkit portfolio transactions [OPTIONS] FILE

   Show portfolio transactions

   Options:
     --output PATH  Save results to CSV file instead of printing to console
     --cash         Show cash transactions instead of asset transactions
     --help         Show this message and exit

**portfolio positions**

.. code-block:: text

   Usage: portfolio-toolkit portfolio positions [OPTIONS] FILE DATE

   Show portfolio positions for a specific date

   Options:
     --plot     Create pie chart visualization
     --country  Group positions by country
     --sector   Group positions by sector
     --help     Show this message and exit

**portfolio performance**

.. code-block:: text

   Usage: portfolio-toolkit portfolio performance [OPTIONS] FILE

   Show performance summary across multiple periods

   Options:
     --display [return|value]        Display mode: returns or values [default: return]
     -n, --periods INTEGER          Number of periods to analyze [default: 4]
     --period-type [weeks|months|quarters|years]  Period type [default: weeks]
     --output PATH                  Save results to CSV file
     --help                         Show this message and exit

**portfolio evolution**

.. code-block:: text

   Usage: portfolio-toolkit portfolio evolution [OPTIONS] FILE

   Plot portfolio evolution over time

   Options:
     --help  Show this message and exit

**portfolio tax-report**

.. code-block:: text

   Usage: portfolio-toolkit portfolio tax-report [OPTIONS] FILE YEAR

   Generate tax report for a specific year

   Options:
     --help  Show this message and exit

Development Usage
-----------------

For development purposes, you can run commands using the module directly:

.. code-block:: bash

   # Using the module directly (for development)
   python -m portfolio_toolkit.cli.cli portfolio transactions portfolio.json
   python -m portfolio_toolkit.cli.cli portfolio positions portfolio.json 2025-07-30
   python -m portfolio_toolkit.cli.cli portfolio performance portfolio.json
   python -m portfolio_toolkit.cli.cli portfolio tax-report portfolio.json 2025

Common Workflows
----------------

**Daily Portfolio Check:**

.. code-block:: bash

   # Check current positions
   portfolio-toolkit portfolio positions portfolio.json $(date +%Y-%m-%d)
   
   # Check recent performance
   portfolio-toolkit portfolio performance portfolio.json --period-type weeks -n 2

**Monthly Review:**

.. code-block:: bash

   # Monthly performance analysis
   portfolio-toolkit portfolio performance portfolio.json --period-type months -n 6
   
   # Export data for spreadsheet analysis
   portfolio-toolkit portfolio transactions portfolio.json --output monthly_transactions.csv
   portfolio-toolkit portfolio performance portfolio.json --output monthly_performance.csv

**Tax Season Preparation:**

.. code-block:: bash

   # Generate tax report
   portfolio-toolkit portfolio tax-report portfolio.json 2025
   
   # Export all transactions for tax software
   portfolio-toolkit portfolio transactions portfolio.json --output tax_transactions.csv

**Portfolio Analysis Session:**

.. code-block:: bash

   # Comprehensive analysis
   portfolio-toolkit portfolio positions portfolio.json $(date +%Y-%m-%d) --plot
   portfolio-toolkit portfolio performance portfolio.json --period-type quarters -n 4
   portfolio-toolkit portfolio evolution portfolio.json

Getting Help
------------

For more help with any command:

.. code-block:: bash

   # General help
   portfolio-toolkit --help

   # Portfolio commands help
   portfolio-toolkit portfolio --help

   # Specific command help
   portfolio-toolkit portfolio transactions --help
   portfolio-toolkit portfolio positions --help
   portfolio-toolkit portfolio performance --help

Error Handling
--------------

The CLI provides helpful error messages for common issues:

**File not found:**

.. code-block:: bash

   $ portfolio-toolkit portfolio positions missing.json 2025-07-30
   Error: Portfolio file 'missing.json' not found.

**Invalid date format:**

.. code-block:: bash

   $ portfolio-toolkit portfolio positions portfolio.json 07-30-2025
   Error: Invalid date format. Use YYYY-MM-DD format.

**Missing arguments:**

.. code-block:: bash

   $ portfolio-toolkit portfolio positions portfolio.json
   Usage: portfolio-toolkit portfolio positions [OPTIONS] FILE DATE
   Error: Missing argument 'DATE'.

For more detailed information about portfolio file formats and data structures, see the :doc:`../user_guide/portfolio_format` documentation.
