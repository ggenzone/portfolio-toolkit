Formato JSON de Cartera
======================

Portfolio Toolkit utiliza un formato JSON estructurado (Versión 2) para almacenar datos de cartera. Este formato soporta transacciones multi-moneda, seguimiento de costos FIFO e historial completo de transacciones.

Resumen de Estructura JSON
--------------------------

El archivo JSON de cartera tiene cuatro secciones principales:

1. **Metadatos de Cartera**: Información básica sobre la cartera
2. **Transacciones**: Array plano de todas las transacciones (depósitos, retiros, compras, ventas)
3. **Divisiones**: Array de eventos de división de acciones (opcional)

Estructura Básica
-----------------

.. code-block:: json

   {
     "name": "Nombre de Cartera",
     "currency": "EUR",
     "transactions": [
       // Array de objetos de transacción
     ],
     "splits": [
       // Array de objetos de división de acciones (opcional)
     ]
   }

Campos de Metadatos de Cartera
------------------------------

name
~~~~
- **Tipo**: String
- **Requerido**: Sí
- **Descripción**: Nombre de visualización para la cartera
- **Ejemplo**: ``"Mi Cartera de Inversiones"``

currency
~~~~~~~~
- **Tipo**: String
- **Requerido**: Sí
- **Descripción**: Moneda base para la cartera (código ISO 4217)
- **Soportadas**: EUR, USD, CAD, GBP, etc.
- **Ejemplo**: ``"EUR"``

Estructura de Transacciones
---------------------------

Cada transacción en el array ``transactions`` debe incluir los siguientes campos:

Campos Principales
~~~~~~~~~~~~~~~~~~

ticker
^^^^^^
- **Tipo**: String o null
- **Requerido**: Sí
- **Descripción**: Símbolo del activo (ej., "AAPL") o ``null`` para transacciones de efectivo
- **Ejemplos**: ``"AAPL"``, ``"GOOGL"``, ``null``

date
^^^^
- **Tipo**: String
- **Requerido**: Sí
- **Formato**: YYYY-MM-DD
- **Descripción**: Fecha de la transacción
- **Ejemplo**: ``"2025-06-12"``

type
^^^^
- **Tipo**: String
- **Requerido**: Sí
- **Valores**: ``"buy"``, ``"sell"``, ``"deposit"``, ``"withdrawal"``
- **Descripción**: Tipo de transacción

quantity
^^^^^^^^
- **Tipo**: Number
- **Requerido**: Sí
- **Descripción**: Número de acciones (valores) o cantidad (efectivo)
- **Ejemplo**: ``10`` (acciones), ``1000.00`` (cantidad de efectivo)

price
^^^^^
- **Tipo**: Number
- **Requerido**: Sí
- **Descripción**: Precio por acción (valores) o ``1.00`` (efectivo)
- **Ejemplo**: ``150.25`` (precio de acción), ``1.00`` (efectivo)

Campos de Moneda y Conversión
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

currency
^^^^^^^^
- **Tipo**: String
- **Requerido**: Sí
- **Descripción**: Moneda de la transacción
- **Ejemplo**: ``"USD"``, ``"EUR"``, ``"CAD"``

total
^^^^^
- **Tipo**: Number
- **Requerido**: Sí
- **Descripción**: Cantidad total en moneda de la transacción
- **Cálculo**: ``quantity × price``
- **Ejemplo**: ``1500.00``

exchange_rate
^^^^^^^^^^^^^
- **Tipo**: Number
- **Requerido**: Sí
- **Descripción**: Tipo de cambio de moneda de transacción a moneda base
- **Formato**: Cuántas unidades de moneda de transacción por 1 unidad de moneda base
- **Ejemplo**: ``1.056`` (tasa EUR/USD)

subtotal_base
^^^^^^^^^^^^^
- **Tipo**: Number
- **Requerido**: Sí
- **Descripción**: Cantidad de transacción en moneda base antes de comisiones
- **Cálculo**: ``total ÷ exchange_rate``
- **Ejemplo**: ``1420.45``

fees_base
^^^^^^^^^
- **Tipo**: Number
- **Requerido**: Sí
- **Descripción**: Comisiones de transacción en moneda base
- **Ejemplo**: ``2.50``

total_base
^^^^^^^^^^
- **Tipo**: Number
- **Requerido**: Sí
- **Descripción**: Costo total en moneda base incluyendo comisiones
- **Cálculo**: ``subtotal_base + fees_base`` (compra) o ``subtotal_base - fees_base`` (venta)
- **Ejemplo**: ``1422.95``

Tipos de Transacciones
----------------------

Compra de Acciones (Buy)
~~~~~~~~~~~~~~~~~~~~~~~~

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

Venta de Acciones (Sell)
~~~~~~~~~~~~~~~~~~~~~~~~

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

Depósito de Efectivo
~~~~~~~~~~~~~~~~~~~

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

Retiro de Efectivo
~~~~~~~~~~~~~~~~~

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

Estructura de Divisiones de Acciones
------------------------------------

El array ``splits`` es opcional y contiene eventos de división de acciones que ajustan automáticamente las posiciones históricas. Cada objeto de división incluye los siguientes campos:

Campos de División
~~~~~~~~~~~~~~~~~

ticker
^^^^^^
- **Tipo**: String
- **Requerido**: Sí
- **Descripción**: Símbolo de la acción que experimentó la división
- **Ejemplo**: ``"EVTL"``, ``"AAPL"``, ``"GOOGL"``

date
^^^^
- **Tipo**: String
- **Requerido**: Sí
- **Formato**: YYYY-MM-DD
- **Descripción**: Fecha en que la división de acciones entró en vigor
- **Ejemplo**: ``"2024-09-23"``

ratio
^^^^^
- **Tipo**: String
- **Requerido**: Sí
- **Descripción**: Proporción de división legible por humanos
- **Formato**: ``"nuevo:viejo"`` (ej., "2:1" para una división de 2 por 1)
- **Ejemplos**: ``"2:1"`` (división), ``"4:1"`` (división), ``"1:10"`` (división inversa)

split_factor
^^^^^^^^^^^^
- **Tipo**: Number
- **Requerido**: Sí
- **Descripción**: Factor numérico para multiplicar las acciones existentes
- **Cálculo**: ``nuevas_acciones = acciones_antiguas × split_factor``
- **Ejemplos**: ``2.0`` (división 2:1), ``0.1`` (división inversa 1:10)

Tipos de División
~~~~~~~~~~~~~~~~

División Directa de Acciones (2:1)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: json

   {
     "ticker": "AAPL",
     "date": "2024-08-31",
     "ratio": "4:1",
     "split_factor": 4.0
   }

**Efecto**: 100 acciones se convierten en 400 acciones, el precio se ajusta de $200 a $50

División Inversa de Acciones (1:10)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: json

   {
     "ticker": "EVTL",
     "date": "2024-09-23",
     "ratio": "1:10",
     "split_factor": 0.1
   }

**Efecto**: 1000 acciones se convierten en 100 acciones, el precio se ajusta de $1 a $10

Procesamiento de Divisiones
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cuando se procesa una división:

1. **Ajuste Automático**: Todas las posiciones mantenidas antes de la fecha de división se ajustan automáticamente
2. **Preservación FIFO**: El sistema mantiene el seguimiento de la base de costos FIFO
3. **Acciones Fraccionarias**: Para divisiones inversas, las acciones fraccionarias se convierten a efectivo
4. **Creación de Transacciones**: El sistema crea transacciones de venta/compra para representar la división

.. note::
   Las divisiones se procesan automáticamente al cargar la cartera. Las transacciones originales permanecen sin cambios, pero los cálculos de posición efectivos tienen en cuenta todas las divisiones.

Ejemplo Completo de División
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Ejemplo Completo
----------------

Aquí hay un archivo JSON de cartera completo con divisiones:

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

Conversión de Comisiones Faltante
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   // ❌ Incorrecto: Comisiones en moneda de transacción
   {
     "currency": "USD",
     "fees_base": 2.50  // Debería convertirse a moneda base
   }

   // ✅ Correcto: Comisiones en moneda base
   {
     "currency": "USD",
     "exchange_rate": 1.056,
     "fees_base": 2.37  // 2.50 USD ÷ 1.056 = 2.37 EUR
   }

Totales Inconsistentes
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   // ❌ Incorrecto: total_base no incluye comisiones
   {
     "subtotal_base": 1000.00,
     "fees_base": 5.00,
     "total_base": 1000.00  // Debería ser 1005.00 para compra
   }

   // ✅ Correcto: total_base incluye comisiones
   {
     "subtotal_base": 1000.00,
     "fees_base": 5.00,
     "total_base": 1005.00  // Para transacciones de compra
   }

Factor de División Incorrecto
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   // ❌ Incorrecto: El factor de división no coincide con la proporción
   {
     "ticker": "AAPL",
     "ratio": "2:1",
     "split_factor": 0.5  // Debería ser 2.0 para una división 2:1
   }

   // ✅ Correcto: El factor de división coincide con la proporción
   {
     "ticker": "AAPL",
     "ratio": "2:1",
     "split_factor": 2.0  // 2 acciones nuevas por 1 acción antigua
   }

   // ✅ Correcto: División inversa
   {
     "ticker": "EVTL",
     "ratio": "1:10",
     "split_factor": 0.1  // 1 acción nueva por 10 acciones antiguas
   }

Mejores Prácticas
----------------

1. **Códigos de Moneda Consistentes**: Usa códigos de moneda ISO 4217 (EUR, USD, CAD)
2. **Tipos de Cambio Precisos**: Usa tipos de cambio de la fecha real de la transacción
3. **Incluir Todas las Comisiones**: Contabiliza todos los costos de transacción en ``fees_base``
4. **Orden Cronológico**: Ordena las transacciones por fecha para facilitar la depuración
5. **Validación**: Usa el script de validación para verificar el formato de tu cartera

Herramientas y Utilidades
-------------------------

Portfolio Toolkit proporciona varias utilidades para trabajar con archivos JSON:

.. code-block:: bash

   # Validar formato de cartera
   python tests/validate_examples.py

   # Analizar y validar cartera usando CLI
   portfolio-toolkit portfolio parse examples/portfolio_example.json

   # Mostrar resumen de cartera con posiciones actuales
   portfolio-toolkit portfolio summary examples/portfolio_example.json

   # Mostrar análisis de rendimiento de cartera
   portfolio-toolkit portfolio performance examples/portfolio_example.json

   # Convertir cartera a diferentes formatos
   portfolio-toolkit portfolio export examples/portfolio_example.json --format csv

También puedes usar el CLI para trabajar con datos de cartera de forma interactiva:

.. code-block:: bash

   # Mostrar todos los comandos de cartera disponibles
   portfolio-toolkit portfolio --help

   # Validar formato de cartera y verificar errores
   portfolio-toolkit portfolio validate examples/portfolio_example.json

   # Mostrar historial detallado de transacciones
   portfolio-toolkit portfolio transactions examples/portfolio_example.json

Para más información sobre comandos CLI, ve la :doc:`Referencia CLI <../cli_reference>`.
