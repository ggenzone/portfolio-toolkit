Comenzando
==========

Esta guía te ayudará a comenzar con Portfolio Toolkit.

Instalación
-----------

Primero, instala Portfolio Toolkit:

.. code-block:: bash

    pip install portfolio-toolkit

Creando tu Primera Cartera
---------------------------

Crea un archivo JSON simple para tu primera cartera:

.. code-block:: json

    {
      "name": "Mi Primera Cartera",
      "currency": "EUR",
      "transactions": [
        {
          "ticker": null,
          "date": "2024-01-01",
          "type": "deposit",
          "quantity": 1000,
          "price": 1.0,
          "currency": "EUR"
        },
        {
          "ticker": "AAPL",
          "date": "2024-01-02",
          "type": "buy",
          "quantity": 5,
          "price": 150.0,
          "currency": "USD",
          "exchange_rate": 0.85
        }
      ]
    }

Uso Básico
----------

Una vez que tengas tu archivo de cartera, puedes usar los comandos básicos:

.. code-block:: bash

    # Ver transacciones
    portfolio-toolkit portfolio transactions mi_cartera.json

    # Ver posiciones actuales
    portfolio-toolkit portfolio positions mi_cartera.json 2024-12-31

    # Analizar rendimiento
    portfolio-toolkit portfolio performance mi_cartera.json

Próximos Pasos
--------------

- Lee la :doc:`portfolio_format` para entender el formato completo
- Revisa los :doc:`../examples/cli_usage` para más ejemplos de CLI
- Explora los :doc:`../examples/basic_usage` para uso programático
