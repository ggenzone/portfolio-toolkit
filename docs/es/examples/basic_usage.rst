Ejemplos de Uso Básico
======================

Esta sección proporciona ejemplos básicos de cómo usar Portfolio Toolkit como biblioteca de Python. Estos ejemplos están basados en el código de trabajo real de los comandos CLI.

Cargar una Cartera
------------------

La forma más común de trabajar con carteras es cargarlas desde archivos JSON usando el cargador integrado:

.. code-block:: python

   from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
   from portfolio_toolkit.portfolio.load_portfolio_json import load_portfolio_json
   from portfolio_toolkit.cli.commands.utils import load_json_file

   # Cargar datos de cartera desde archivo JSON
   data = load_json_file('portfolio.json')
   
   # Crear un proveedor de datos de Yahoo Finance
   data_provider = YFDataProvider()
   
   # Cargar la cartera con datos de mercado
   portfolio = load_portfolio_json(data, data_provider=data_provider)

   # Imprimir información básica de la cartera
   print(f"Nombre de Cartera: {portfolio.name}")
   print(f"Moneda Base: {portfolio.currency}")
   print(f"Número de Activos: {len(portfolio.assets)}")

Para el formato JSON de cartera, ve :doc:`../user_guide/portfolio_format`.

Ver Transacciones de Cartera
-----------------------------

Puedes ver y exportar transacciones de cartera de diferentes maneras:

**Transacciones de Activos**

.. code-block:: python

   from portfolio_toolkit.asset.portfolio_asset import PortfolioAsset

   # Obtener todas las transacciones de activos como DataFrame
   transactions_df = PortfolioAsset.to_dataframe(portfolio.assets)
   print(transactions_df)

   # Exportar a CSV
   transactions_df.to_csv('asset_transactions.csv', index=False)
   print("Transacciones de activos exportadas a CSV")

**Transacciones de Efectivo**

.. code-block:: python

   from portfolio_toolkit.account.account import Account

   # Obtener transacciones de cuenta de efectivo como DataFrame
   cash_df = Account.to_dataframe(portfolio.account)
   print(cash_df)

   # Exportar a CSV
   cash_df.to_csv('cash_transactions.csv', index=False)
   print("Transacciones de efectivo exportadas a CSV")

Salida de ejemplo:

.. code-block:: text

   📊 Transacciones de activos de cartera
   ============================================================
   ticker    date        type  quantity     price currency
   AAPL   2023-01-20     buy      50.0    150.25      USD
   MSFT   2023-02-10     buy      30.0    280.50      USD

Ver Posiciones Actuales
-----------------------

Obtener posiciones abiertas para una fecha específica:

.. code-block:: python

   from portfolio_toolkit.position.get_open_positions import get_open_positions
   from portfolio_toolkit.position.print_open_positions import print_open_positions
   from portfolio_toolkit.position.valued_position import ValuedPosition

   # Obtener posiciones abiertas para una fecha específica
   date_str = "2025-07-30"
   open_positions = get_open_positions(portfolio.assets, date_str)

   # Imprimir posiciones en consola
   print_open_positions(open_positions)

   # Convertir a DataFrame para análisis
   positions_df = ValuedPosition.to_dataframe(open_positions)
   print(positions_df)

   # Exportar posiciones a CSV
   positions_df.to_csv('current_positions.csv')

Salida de ejemplo:

.. code-block:: text

   📊 Posiciones Abiertas al 2025-07-30
   ============================================================
   Ticker  Cantidad  Precio Actual  Valor Mercado  Ganancia/Pérdida (%)
   AAPL         50         208.62      10,431.00         +38.5%
   MSFT         30         445.91      13,377.30         +59.2%

Análisis de Rendimiento
-----------------------

Analizar el rendimiento de la cartera a través de múltiples períodos de tiempo:

.. code-block:: python

   from portfolio_toolkit.position.compare_open_positions import compare_open_positions
   from portfolio_toolkit.utils import get_last_periods

   # Obtener las últimas 4 semanas para comparación
   periods = get_last_periods(n=4, period_type='weeks', include_current=True)

   # Comparar posiciones a través de estos períodos
   comparison_df = compare_open_positions(portfolio, periods, display='return')
   print("Comparación de rendimiento (retornos):")
   print(comparison_df)

   # Comparar valores de posición en lugar de retornos
   values_df = compare_open_positions(portfolio, periods, display='value')
   print("Comparación de valores de posición:")
   print(values_df)

   # Exportar datos de rendimiento
   comparison_df.to_csv('performance_analysis.csv')

Salida de ejemplo:

.. code-block:: text

   📊 Resumen de Rendimiento - Últimas 4 Semanas
   ============================================================
           S27 2025    S28 2025    S29 2025    S30 2025
   AAPL    -           3.33%       2.86%       1.92%
   MSFT    -           -1.25%      4.17%       2.10%
   ============================================================

Visualizar Datos de Cartera
---------------------------

Create visualizations of your portfolio:

**Position Charts**

.. code-block:: python

   from portfolio_toolkit.position.plot_open_positions import plot_open_positions
   from portfolio_toolkit.plot.engine import PlotEngine

   # Get open positions
   date_str = "2025-07-30"
   open_positions = get_open_positions(portfolio.assets, date_str)

   # Create pie chart of positions
   chart_data = plot_open_positions(open_positions, group_by="Ticker")
   PlotEngine.plot(chart_data)

   # Group by country
   country_chart = plot_open_positions(open_positions, group_by="Country")
   PlotEngine.plot(country_chart)

   # Group by sector
   sector_chart = plot_open_positions(open_positions, group_by="Sector")
   PlotEngine.plot(sector_chart)

**Portfolio Evolution**

.. code-block:: python

   from portfolio_toolkit.portfolio.plot_evolution import plot_portfolio_evolution
   from portfolio_toolkit.portfolio.time_series_portfolio import create_time_series_portfolio_from_portfolio

   # Create time series portfolio for plotting
   ts_portfolio = create_time_series_portfolio_from_portfolio(portfolio)

   # Plot portfolio evolution over time
   line_data = plot_portfolio_evolution(ts_portfolio)
   PlotEngine.plot(line_data)

Working with Period Utilities
-----------------------------

Use the period utilities for time-based analysis:

.. code-block:: python

   from portfolio_toolkit.utils.period import get_current_period, get_last_periods, Period

   # Get current period
   current_week = get_current_period('week')
   current_month = get_current_period('month')
   current_quarter = get_current_period('quarter')
   current_year = get_current_period('year')

   print(f"Current week: {current_week.label}")
   print(f"Period: {current_week.start_date} to {current_week.end_date}")

   # Get last periods
   last_quarters = get_last_periods(n=4, period_type='quarters', include_current=False)
   
   for period in last_quarters:
       print(f"{period.label}: {period.start_date} to {period.end_date}")

   # Create custom period
   custom_period = Period(
       label="Q1 2025",
       start_date=date(2025, 1, 1),
       end_date=date(2025, 3, 31)
   )

Error Handling
--------------

Handle common errors when working with portfolio data:

.. code-block:: python

   try:
       # Load portfolio
       data = load_json_file('portfolio.json')
       portfolio = load_portfolio_json(data, data_provider)
       
   except FileNotFoundError:
       print("Portfolio file not found")
       
   except ValueError as e:
       print(f"Invalid portfolio format: {e}")
       
   except Exception as e:
       print(f"Error loading portfolio: {e}")

   try:
       # Get positions for invalid date
       positions = get_open_positions(portfolio.assets, "invalid-date")
       
   except ValueError as e:
       print(f"Invalid date format: {e}")

Data Export Patterns
--------------------

Common patterns for exporting data:

.. code-block:: python

   # Export with conditional logic
   def export_data(data_df, output_file=None):
       if output_file:
           data_df.to_csv(output_file, index=False)
           print(f"✅ Results saved to: {output_file}")
       else:
           print(data_df.to_string())

   # Usage examples
   positions_df = ValuedPosition.to_dataframe(open_positions)
   export_data(positions_df, 'positions.csv')  # Save to file
   export_data(positions_df)                   # Print to console

Complete Analysis Example
-------------------------

Here's a complete example that performs comprehensive portfolio analysis:

.. code-block:: python

   from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
   from portfolio_toolkit.portfolio.load_portfolio_json import load_portfolio_json
   from portfolio_toolkit.position.get_open_positions import get_open_positions
   from portfolio_toolkit.position.compare_open_positions import compare_open_positions
   from portfolio_toolkit.utils import get_last_periods
   from portfolio_toolkit.cli.commands.utils import load_json_file
   from datetime import date

   def comprehensive_analysis(portfolio_path, analysis_date="2025-07-30"):
       """
       Perform comprehensive portfolio analysis
       """
       # Load portfolio
       data = load_json_file(portfolio_path)
       data_provider = YFDataProvider()
       portfolio = load_portfolio_json(data, data_provider=data_provider)
       
       print(f"=== Portfolio Analysis: {portfolio.name} ===")
       print(f"Base Currency: {portfolio.currency}")
       print(f"Analysis Date: {analysis_date}")
       print("=" * 50)
       
       # 1. Current positions
       print("\\n📊 Current Positions:")
       open_positions = get_open_positions(portfolio.assets, analysis_date)
       positions_df = ValuedPosition.to_dataframe(open_positions)
       print(positions_df.to_string())
       
       # 2. Performance analysis
       print("\\n📈 Performance Analysis (Last 4 Weeks):")
       periods = get_last_periods(n=4, period_type='weeks', include_current=True)
       performance_df = compare_open_positions(portfolio, periods, display='return')
       print(performance_df.to_string())
       
       # 3. Asset transactions summary
       print("\\n💰 Asset Transactions:")
       from portfolio_toolkit.asset.portfolio_asset import PortfolioAsset
       transactions_df = PortfolioAsset.to_dataframe(portfolio.assets)
       print(f"Total transactions: {len(transactions_df)}")
       print(transactions_df.head().to_string())
       
       # 4. Cash transactions summary
       print("\\n🏦 Cash Account:")
       from portfolio_toolkit.account.account import Account
       cash_df = Account.to_dataframe(portfolio.account)
       print(f"Total cash transactions: {len(cash_df)}")
       
       # 5. Export all data
       positions_df.to_csv('analysis_positions.csv', index=False)
       performance_df.to_csv('analysis_performance.csv')
       transactions_df.to_csv('analysis_transactions.csv', index=False)
       cash_df.to_csv('analysis_cash.csv', index=False)
       
       print("\\n✅ Analysis complete. Data exported to CSV files.")
       return portfolio

   # Run the analysis
   if __name__ == "__main__":
       portfolio = comprehensive_analysis('portfolio.json')

Best Practices
--------------

1. **Always use data providers**: Don't load portfolios without a data provider:

   .. code-block:: python

      # Good
      data_provider = YFDataProvider()
      portfolio = load_portfolio_json(data, data_provider=data_provider)

2. **Handle date formats consistently**: Use YYYY-MM-DD format for dates:

   .. code-block:: python

      # Good
      positions = get_open_positions(portfolio.assets, "2025-07-30")

3. **Export data conditionally**: Allow both console output and file export:

   .. code-block:: python

      def display_or_export(df, output_file=None):
          if output_file:
              df.to_csv(output_file, index=False)
              print(f"✅ Saved to {output_file}")
          else:
              print(df.to_string())

4. **Use DataFrame conversions**: Most portfolio objects have `to_dataframe()` methods:

   .. code-block:: python

      # Convert to DataFrame for analysis
      df = ValuedPosition.to_dataframe(positions)
      summary_stats = df.describe()

5. **Period utilities for time analysis**: Use the period utilities for consistent time handling:

   .. code-block:: python

      # Get periods consistently
      periods = get_last_periods(n=6, period_type='months', include_current=True)

This documentation shows you how to use the Portfolio Toolkit library based on the actual working code from the CLI commands, ensuring that all examples will work correctly.
