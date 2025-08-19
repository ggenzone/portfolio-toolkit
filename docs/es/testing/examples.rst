Ejemplos de Pruebas
===================

Esta sección contiene ejemplos de cómo probar Portfolio Toolkit.

Ejecutar las Pruebas
--------------------

Para ejecutar todas las pruebas:

.. code-block:: bash

    pytest

Para ejecutar pruebas específicas de un módulo:

.. code-block:: bash

    pytest tests/portfolio/
    pytest tests/asset/
    pytest tests/account/

Pruebas de Cobertura
--------------------

Para generar un reporte de cobertura:

.. code-block:: bash

    pytest --cov=portfolio_toolkit --cov-report=html

Ejemplos de Casos de Prueba
---------------------------

**Probar carga de cartera:**

.. code-block:: python

    import pytest
    from portfolio_toolkit.portfolio.load_portfolio_json import load_portfolio_json
    from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
    
    def test_load_portfolio():
        data = {
            "name": "Test Portfolio",
            "currency": "USD",
            "transactions": []
        }
        
        data_provider = YFDataProvider()
        portfolio = load_portfolio_json(data, data_provider=data_provider)
        
        assert portfolio.name == "Test Portfolio"
        assert portfolio.currency == "USD"

**Probar transacciones:**

.. code-block:: python

    def test_portfolio_transaction():
        # Datos de prueba para transacciones
        transaction_data = {
            "ticker": "AAPL",
            "date": "2024-01-01",
            "type": "buy",
            "quantity": 10,
            "price": 150.0,
            "currency": "USD"
        }
        
        # Probar creación de transacción
        # ... código de prueba
