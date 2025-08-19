Documentación de Portfolio Tools
===============================

.. raw:: html

   <div style="background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 6px; padding: 16px; margin-bottom: 24px; text-align: center;">
      <span style="margin-right: 12px;">🌐</span>
      <strong>Language / Idioma:</strong>
      <a href="../" style="color: #0366d6; text-decoration: none; font-weight: 500;">English</a>
      <span style="margin: 0 8px;">Español (actual)</span>
   </div>

.. image:: https://img.shields.io/badge/python-3.9%2B-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Versión de Python

.. image:: https://img.shields.io/github/license/ggenzone/portfolio-toolkit.svg
   :target: https://github.com/ggenzone/portfolio-toolkit/blob/main/LICENSE
   :alt: Licencia

.. image:: https://img.shields.io/badge/docs-sphinx-brightgreen.svg
   :target: https://ggenzone.github.io/portfolio-toolkit/
   :alt: Documentación

Portfolio Toolkit es una biblioteca completa de Python para gestión, análisis y visualización de carteras. Soporta carteras multi-moneda con conversión automática de divisas, cálculo de costos FIFO y análisis avanzados.

Características
---------------

* **Soporte Multi-Moneda**: Maneja carteras con transacciones en diferentes divisas (USD, EUR, CAD, etc.)
* **Cálculo de Costos FIFO**: Seguimiento preciso de base de costo usando metodología First-In-First-Out
* **Conversión Automática de Divisas**: Conversión de divisas en tiempo real con tipos de cambio configurables
* **Análisis de Carteras**: Herramientas de análisis integral incluyendo rendimientos, composición y seguimiento de evolución
* **Visualización de Datos**: Capacidades de gráficos enriquecidas para análisis de composición y rendimiento de carteras
* **Exportación CSV**: Exporta datos de transacciones y posiciones de carteras a formato CSV
* **Interfaz CLI**: Herramientas de línea de comandos potentes construidas con Click para análisis de carteras, visualización de datos e investigación de mercados

Inicio Rápido
--------------

Instalación
~~~~~~~~~~~~

.. code-block:: bash

   pip install portfolio-toolkit

Uso Básico (CLI)
~~~~~~~~~~~~~~~~~

La forma más fácil de comenzar es usando la interfaz de línea de comandos:

.. code-block:: bash

   # Ver comandos disponibles
   portfolio-toolkit --help

   # Mostrar posiciones actuales de la cartera
   portfolio-toolkit portfolio positions portfolio.json 2025-07-30

   # Ver transacciones de la cartera
   portfolio-toolkit portfolio transactions portfolio.json

   # Analizar rendimiento en el tiempo
   portfolio-toolkit portfolio performance portfolio.json

   # Generar gráfico de evolución de la cartera
   portfolio-toolkit portfolio evolution portfolio.json

Uso de la Biblioteca
~~~~~~~~~~~~~~~~~~~~

Para acceso programático, puedes usar la biblioteca de Python:

.. code-block:: python

   from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
   from portfolio_toolkit.portfolio.load_portfolio_json import load_portfolio_json
   from portfolio_toolkit.cli.commands.utils import load_json_file

   # Cargar cartera
   data = load_json_file('portfolio.json')
   data_provider = YFDataProvider()
   portfolio = load_portfolio_json(data, data_provider=data_provider)

Para uso detallado de la biblioteca, ve :doc:`examples/basic_usage`.

Formato JSON de Cartera
~~~~~~~~~~~~~~~~~~~~~~~

Crea un archivo JSON de cartera para empezar. Para documentación detallada del formato, ve :doc:`user_guide/portfolio_format`.

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

Interfaz de Línea de Comandos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El CLI proporciona herramientas poderosas para el análisis de cartera:

.. code-block:: bash

   # Comandos de análisis de cartera
   portfolio-toolkit portfolio transactions portfolio.json              # Ver transacciones
   portfolio-toolkit portfolio positions portfolio.json 2025-07-30     # Posiciones actuales
   portfolio-toolkit portfolio performance portfolio.json               # Análisis de rendimiento
   portfolio-toolkit portfolio evolution portfolio.json                 # Gráfico de evolución

   # Opciones de exportación
   portfolio-toolkit portfolio transactions portfolio.json --output transactions.csv
   portfolio-toolkit portfolio performance portfolio.json --output performance.csv

   # Análisis de rendimiento con diferentes períodos de tiempo
   portfolio-toolkit portfolio performance portfolio.json --period-type months -n 6
   portfolio-toolkit portfolio performance portfolio.json --period-type quarters -n 4

Para documentación completa del CLI, ve :doc:`examples/cli_usage`.


Ejemplos
--------

.. toctree::
   :maxdepth: 2
   :caption: Ejemplos

   examples/cli_usage
   examples/basic_usage
   examples/multi_currency

Guía de Usuario
---------------

.. toctree::
   :maxdepth: 2
   :caption: Guía de Usuario

   user_guide/installation
   user_guide/getting_started
   user_guide/watchlist_format
   user_guide/optimization_format
   user_guide/portfolio_format


Referencia de API
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Documentación de API

   api/portfolio_toolkit
   api/modules

Pruebas
-------

.. toctree::
   :maxdepth: 2
   :caption: Pruebas

   testing/examples
   testing/validation

Índices y Tablas
================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
