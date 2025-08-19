Validación
==========

Esta sección describe los métodos de validación en Portfolio Toolkit.

Validación de Datos
-------------------

Portfolio Toolkit incluye validación automática para:

- Formato de fecha (YYYY-MM-DD)
- Tipos de transacción válidos
- Campos requeridos
- Coherencia de datos

**Ejemplo de validación:**

.. code-block:: python

    from portfolio_toolkit.portfolio.portfolio_from_dict import portfolio_from_dict
    
    # Datos inválidos causarán errores de validación
    invalid_data = {
        "name": "Test",
        "currency": "INVALID",  # Moneda inválida
        "transactions": [
            {
                "ticker": "AAPL",
                "date": "invalid-date",  # Formato de fecha inválido
                "type": "invalid_type",  # Tipo de transacción inválido
                "quantity": -10,  # Cantidad negativa
                "price": 0,  # Precio cero
                "currency": "USD"
            }
        ]
    }

Herramientas de Validación
--------------------------

**Validación desde CLI:**

.. code-block:: bash

    # El CLI automáticamente valida archivos
    portfolio-toolkit portfolio validate mi_cartera.json

**Validación programática:**

.. code-block:: python

    try:
        portfolio = load_portfolio_json(data, data_provider)
        print("Datos válidos")
    except ValidationError as e:
        print(f"Error de validación: {e}")

Casos Edge
----------

- Transacciones con cantidad cero
- Fechas futuras
- Divisiones de acciones inconsistentes
- Monedas no soportadas
- Datos faltantes
