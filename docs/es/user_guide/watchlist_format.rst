Formato JSON de Lista de Seguimiento
====================================

Portfolio Toolkit utiliza un formato JSON estructurado para almacenar listas de seguimiento de activos. Este formato es mucho más simple que el formato de Cartera y está diseñado para facilitar el seguimiento y monitoreo de activos.

Resumen de Estructura JSON
--------------------------

El archivo JSON de Lista de Seguimiento tiene dos secciones principales:

1. **Metadatos de Lista de Seguimiento**: Información básica sobre la lista de activos
2. **Activos**: Un array de objetos que representan los activos a rastrear

Estructura Básica
-----------------

.. code-block:: json

   {
     "name": "Nombre de Lista de Seguimiento",
     "currency": "USD",
     "assets": [
       { "ticker": "AAPL" },
       { "ticker": "GOOGL" },
       { "ticker": "MSFT" }
     ]
   }

Campos de Metadatos de Lista de Seguimiento
-------------------------------------------

name
~~~~
- **Tipo**: String
- **Requerido**: Sí
- **Descripción**: Nombre de visualización para la lista de seguimiento
- **Ejemplo**: ``"Lista de Seguimiento de Acciones Tech"``

currency
~~~~~~~~
- **Tipo**: String
- **Requerido**: Sí
- **Descripción**: Moneda base para la lista de seguimiento (código ISO 4217)
- **Soportadas**: USD, EUR, CAD, GBP, etc.
- **Ejemplo**: ``"USD"``

Estructura de Activos
---------------------

Cada objeto en el array ``assets`` debe incluir el siguiente campo:

ticker
^^^^^^
- **Tipo**: String
- **Requerido**: Sí
- **Descripción**: Símbolo del activo (ej., "AAPL", "GOOGL")
- **Ejemplo**: ``"AAPL"``

Ejemplo Completo
----------------

Aquí hay un ejemplo completo de un archivo JSON de Lista de Seguimiento:

.. code-block:: json

   {
     "name": "Lista de Seguimiento de Acciones Tech",
     "currency": "USD",
     "assets": [
       { "ticker": "AAPL" },
       { "ticker": "GOOGL" },
       { "ticker": "MSFT" },
       { "ticker": "AMZN" }
     ]
   }

Reglas de Validación
--------------------

Se aplican las siguientes reglas de validación:

Campos Requeridos
~~~~~~~~~~~~~~~~
- Todos los campos listados arriba son requeridos
- Ningún campo puede ser ``null``

Tipos de Datos
~~~~~~~~~~~~~~
- ``name`` y ``currency`` deben ser strings no vacíos
- ``ticker`` debe ser un string válido

Consistencia Lógica
~~~~~~~~~~~~~~~~~~~
- ``currency`` debe ser un código ISO 4217 válido
- Los valores de ``ticker`` deben ser únicos dentro de la lista de seguimiento

Mejores Prácticas
-----------------

1. **Códigos de Moneda Consistentes**: Usa códigos de moneda ISO 4217 (USD, EUR, CAD)
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