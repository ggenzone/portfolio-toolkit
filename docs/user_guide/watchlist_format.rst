Watchlist JSON Format
=====================

Portfolio Tools utiliza un formato JSON estructurado para almacenar listas de activos (Watchlist). Este formato es mucho más simple que el de Portfolio y está diseñado para facilitar el seguimiento de activos.

JSON Structure Overview
------------------------

El archivo JSON de Watchlist tiene tres secciones principales:

1. **Watchlist Metadata**: Información básica sobre la lista de activos.
2. **Assets**: Un listado de objetos que representan los activos.

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
- **Description**: Nombre de la lista de activos.
- **Example**: ``"Tech Stocks Watchlist"``

currency
~~~~~~~~
- **Type**: String
- **Required**: Yes
- **Description**: Moneda base para la lista de activos (ISO 4217 code).
- **Supported**: USD, EUR, CAD, GBP, etc.
- **Example**: ``"USD"``

Assets Structure
----------------

Cada objeto en el array ``assets`` debe incluir el siguiente campo:

ticker
^^^^^^
- **Type**: String
- **Required**: Yes
- **Description**: Símbolo del activo (e.g., "AAPL", "GOOGL").
- **Example**: ``"AAPL"``

Complete Example
----------------

Aquí tienes un ejemplo completo de un archivo JSON de Watchlist:

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

Las siguientes reglas de validación aplican:

Required Fields
~~~~~~~~~~~~~~~
- Todos los campos listados arriba son obligatorios.
- Ningún campo puede ser ``null``.

Data Types
~~~~~~~~~~
- ``name`` y ``currency`` deben ser cadenas de texto no vacías.
- ``ticker`` debe ser una cadena de texto válida.

Logical Consistency
~~~~~~~~~~~~~~~~~~~
- ``currency`` debe ser un código ISO 4217 válido.
- Los valores de ``ticker`` deben ser únicos dentro de la lista.

Best Practices
--------------

1. **Consistent Currency Codes**: Usa códigos ISO 4217 (USD, EUR, CAD).
2. **Unique Tickers**: Evita duplicados en la lista de activos.
3. **Validation**: Usa herramientas para validar el formato de tu Watchlist.

Tools and Utilities
-------------------

Portfolio Tools proporciona utilidades para trabajar con archivos JSON de Watchlist:

.. code-block:: bash

   # Validar el formato de Watchlist
   python validate_watchlist.py