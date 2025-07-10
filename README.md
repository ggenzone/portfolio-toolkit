# Finanzas Library Documentation

This library provides tools for financial analysis, portfolio management, and market data visualization.

## Installation

```bash
pip install -r requirements.txt
```

## Main Modules

### Portfolio

The `Portfolio` class allows you to manage and analyze an investment portfolio.

#### Initialization

```python
from portfolio.portfolio import Portfolio
from data_provider.yf_data_provider import YFDataProvider

# Create the data provider
data_provider = YFDataProvider()

# Load portfolio from JSON
portfolio = Portfolio(json_filepath="portfolio_example.json", data_provider=data_provider)
```

#### Visualization

```python
# Pie chart of current portfolio composition
df = portfolio.df_portfolio
from portfolio.plot import plot_composition, plot_evolution_ticker, plot_evolution_vs_cost, plot_evolution_stacked
plot_composition(df)

# Evolution of a specific ticker
plot_evolution_ticker(df, ticker='AAPL')

# Evolution of portfolio value vs cost
plot_evolution_vs_cost(df)

# Stacked area chart of composition
df = portfolio.df_portfolio
plot_evolution_stacked(df)
```

### Data Provider

The `YFDataProvider` module provides access to historical market data using Yahoo Finance.

#### Initialization and Basic Usage

```python
from data_provider.yf_data_provider import YFDataProvider

# Create instance
data_provider = YFDataProvider()

# Get price for a specific date
from datetime import datetime
date = datetime(2022, 6, 1)
price = data_provider.get_price('AAPL', date)

# Get full price series
prices = data_provider.get_price_series('AAPL')

# Get raw data (includes Open, High, Low, Close, Volume)
data = data_provider.get_raw_data('AAPL', period="5y")
```

#### Return and Correlation Analysis

```python
from math.log_returns import calculate_log_returns
from math.correlation import calculate_correlation

# Calculate log returns
returns_aapl = calculate_log_returns(data_provider.get_price_series('AAPL'))
returns_msft = calculate_log_returns(data_provider.get_price_series('MSFT'))

# Calculate correlation between assets
correlation = calculate_correlation(returns_aapl, returns_msft)
print(f"Correlation between AAPL and MSFT: {correlation}")
```

### Common Tickers

```python
# Indices
NASDAQ = "^IXIC"
SP500 = "^GSPC"
DOW_JONES = "^DJI"
MERVAL = "^MERV"

# Commodities
BRENT = "BZ=F"
WTI = "CL=F"
ORO = "GC=F"

# Others
BONO_10_ANIOS_USA = "^TNX"
DOLAR_INDEX = "DX-Y.NYB"
VIX = "^VIX"
```

### Predefined Tickers in DataProvider

Index, stock, and currency ticker constants are available as class attributes in any compatible DataProvider instance (e.g., YFDataProvider):

```python
# Example usage of predefined tickers
prices_aapl = data_provider.get_price_series(data_provider.AAPL)
prices_sp500 = data_provider.get_price_series(data_provider.SP500)
prices_usdars = data_provider.get_price_series(data_provider.USDARS)
```

This allows code to be agnostic to the data provider type and makes it easy to access major financial assets.

## Portfolio JSON Structure

The JSON file to load a portfolio must have the following structure:

```json
[
  {
    "ticker": "AAPL",
    "transactions": [
      {
        "date": "2023-03-15",
        "type": "buy",
        "quantity": 100,
        "price": 150.25,
        "currency": "USD",
        "total": 15025.00,
        "exchange_rate": 1.0876,
        "subtotal_eur": 13814.82,
        "fees_eur": 34.54,
        "total_eur": 13849.36
      }
    ],
    "sector": "Technology",
    "country": "USA"
  }
]
```

## Data Provider Functionality

- `YFDataProvider` implements a cache system to optimize queries.
- Downloaded data is stored in the `temp/` folder with the format `YYYYMMDD-TICKER_historical_data.pkl`
- If data already exists in the cache for the current day, it will be used instead of downloading again.

## Visualization Functions

Visualization functions use `matplotlib` and are designed to provide different views of the data:

- `plot_composition()`: Shows a pie chart with the current portfolio composition
- `plot_evolution_ticker()`: Shows the evolution of value and cost for a specific ticker
- `plot_evolution_vs_cost()`: Compares the total value of the portfolio against its cost
- `plot_evolution_stacked()`: Shows a stacked area chart with the evolution of all assets

## Analysis Examples

### Correlation Analysis Between Assets

```python
from data_provider.yf_data_provider import YFDataProvider
from math.log_returns import calculate_log_returns
from math.correlation import calculate_correlation

data_provider = YFDataProvider()
tickers = ['AAPL', 'MSFT', 'GOOGL']
returns = {ticker: calculate_log_returns(data_provider.get_price_series(ticker)) for ticker in tickers}

for i in range(len(tickers)):
    for j in range(i+1, len(tickers)):
        corr = calculate_correlation(returns[tickers[i]], returns[tickers[j]])
        print(f"Correlation between {tickers[i]} and {tickers[j]}: {corr:.2f}")
```

### Portfolio Analysis

```python
# Get the current value of the portfolio
dates, values = portfolio.calculate_value()
print(f"Current portfolio value: ${values[-1]:,.2f}")

# Analyze composition by sector
from portfolio.plot import plot_composition
plot_composition(portfolio.df_portfolio, group_by="sector")
```

## CLI

The project includes a command-line interface (`cli.py`) to facilitate common tasks without programming.

### Usage Example

```bash
python cli.py -v
```
Shows the CLI version.

```bash
python cli.py composition -f portfolio.json
```
Plots the composition of the portfolio defined in the file `portfolio.json`.

```bash
python cli.py correlation -t AAPL,MSFT,GOOGL
```
Calculates the correlation between all pairs of the specified tickers.

```bash
python cli.py plot -t AAPL,MSFT,GOOGL
```
Plots the price evolution of the specified assets, showing their historical prices in a single chart.

```bash
python cli.py print-positions -f portfolio.json
```
Prints a table of current portfolio positions from the file `portfolio.json`.

```bash
python cli.py clear-cache
```
Deletes all cache files in the `temp/` directory (files ending with `.pkl`).

### Available commands

- `composition`: Plots the portfolio composition.
  - `-f`, `--file`: Path to the portfolio file in JSON format (required).
- `correlation`: Calculates the correlation between all pairs of a list of tickers.
  - `-t`, `--tickers`: Comma-separated list of tickers (e.g. AAPL,MSFT,GOOGL) (required).
- `plot`: Plots the price evolution of a list of assets.
  - `-t`, `--tickers`: Comma-separated list of tickers (e.g. AAPL,MSFT,GOOGL) (required).
- `print-positions`: Prints a table of current portfolio positions.
  - `-f`, `--file`: Path to the portfolio file in JSON format (required).
- `clear-cache`: Deletes all cache files in the `temp/` directory.
- `-v`, `--version`: Shows the CLI version.
- `ticker-info`: Shows detailed information for a ticker in a formatted table.
  - `-t`, `--ticker`: Ticker symbol (e.g. AAPL) (required).

You can extend the CLI by adding more commands in the `cli.py` file and the `commands/` folder.

## To Do

- [ ] Add support for more data providers (e.g., Alpha Vantage, IEX Cloud)
- [ ] Allow loading portfolios from Excel and ODS files natively
- [ ] Improve error handling and input data validation
- [ ] Add unit and integration tests for all modules
- [ ] Implement portfolio performance metrics (Sharpe, Sortino, drawdown, etc.)
- [ ] Add interactive visualizations (e.g., with Plotly or Dash)
- [ ] Support multi-currency portfolios and automatic currency conversion
- [ ] Document all public methods with usage examples
- [ ] Add export to PDF/Excel reports
- [ ] Allow portfolio rebalancing and optimization simulations
- [ ] Add risk analysis and Value at Risk (VaR)
- [ ] Improve CLI interface for task automation
