Formato JSON de Optimización
============================

Portfolio Toolkit utiliza un formato JSON estructurado para almacenar datos de optimización de cartera. Este formato es similar al formato de Lista de Seguimiento, pero permite incluir cantidades (`quantity`) para cada activo, lo que facilita el análisis y optimización.

Resumen de Estructura JSON
--------------------------

El archivo JSON de Optimización tiene dos secciones principales:

1. **Metadatos de Optimización**: Información básica sobre la optimización
2. **Activos**: Un array de objetos que representan los activos, con cantidades opcionales

Estructura Básica
-----------------

.. code-block:: json

   {
     "name": "Nombre de Optimización",
     "currency": "USD",
     "assets": [
       { "ticker": "AAPL", "quantity": 50 },
       { "ticker": "GOOGL" },
       { "ticker": "MSFT", "quantity": 30 }
     ]
   }

Campos de Metadatos de Optimización
-----------------------------------

name
~~~~
- **Tipo**: String
- **Requerido**: Sí
- **Descripción**: Nombre de visualización para la optimización
- **Ejemplo**: ``"Optimización de Cartera Tech"``

currency
~~~~~~~~
- **Tipo**: String
- **Requerido**: Sí
- **Descripción**: Moneda base para la optimización (código ISO 4217)
- **Soportadas**: USD, EUR, CAD, GBP, etc.
- **Ejemplo**: ``"USD"``

Estructura de Activos
---------------------

Cada objeto en el array ``assets`` puede incluir los siguientes campos:

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