Optimization JSON Format
========================

Portfolio Tools utiliza un formato JSON estructurado para almacenar datos de optimización de carteras. Este formato es similar al de Watchlist, pero permite incluir cantidades (`quantity`) para cada activo, lo que facilita el análisis y la optimización.

JSON Structure Overview
------------------------

El archivo JSON de Optimization tiene tres secciones principales:

1. **Optimization Metadata**: Información básica sobre la optimización.
2. **Assets**: Un listado de objetos que representan los activos, con la opción de incluir cantidades.

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
- **Description**: Nombre de la optimización.
- **Example**: ``"Tech Portfolio Optimization"``

currency
~~~~~~~~
- **Type**: String
- **Required**: Yes
- **Description**: Moneda base para la optimización (ISO 4217 code).
- **Supported**: USD, EUR, CAD, GBP, etc.
- **Example**: ``"USD"``

Assets Structure
----------------

Cada objeto en el array ``assets`` puede incluir los siguientes campos:

ticker
^^^^^^
- **Type**: String
- **Required**: Yes
- **Description**: Símbolo del activo (e.g., "AAPL", "GOOGL").
- **Example**: ``"AAPL"``

quantity
^^^^^^^^
- **Type**: Float
- **Required**: No
- **Description**: Cantidad del activo para análisis y optimización.
- **Example**: ``50``

Complete Example
----------------

Aquí tienes un ejemplo completo de un archivo JSON de Optimization:

.. code-block:: json

   {
     "name": "Tech Portfolio Optimization",
     "currency": "USD",
     "assets": [
       { "ticker": "AAPL", "quantity": 50 },
       { "ticker": "GOOGL" },
       { "ticker": "MSFT", "quantity": 30 },
       { "ticker": "AMZN" }
     ]
   }

Validation Rules
----------------

Las siguientes reglas de validación aplican:

Required Fields
~~~~~~~~~~~~~~~
- Todos los campos listados arriba son obligatorios, excepto `quantity`.

Data Types
~~~~~~~~~~
- ``name`` y ``currency`` deben ser cadenas de texto no vacías.
- ``ticker`` debe ser una cadena de texto válida.
- ``quantity`` debe ser un número flotante positivo si está presente.

Logical Consistency
~~~~~~~~~~~~~~~~~~~
- ``currency`` debe ser un código ISO 4217 válido.
- Los valores de ``ticker`` deben ser únicos dentro de la lista.

Best Practices
--------------

1. **Consistent Currency Codes**: Usa códigos ISO 4217 (USD, EUR, CAD).
2. **Unique Tickers**: Evita duplicados en la lista de activos.
3. **Optional Quantities**: Incluye `quantity` solo si es relevante para el análisis.

Tools and Utilities
-------------------

Portfolio Tools proporciona utilidades para trabajar con archivos JSON de Optimization:

.. code-block:: bash

   # Validar el formato de Optimization
   python validate_optimization.py