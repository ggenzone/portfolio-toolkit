# Portfolio-tools Library Documentation

This library provides tools for financial analysis, portfolio management, and market data visualization.

## Installation

Install from the project root (local development):

```bash
pip install .
```
Or in editable mode (recommended for development):
```bash
pip install -e .
```

To uninstall:
```bash
pip uninstall portfolio-tools
```

## Command Line Interface (CLI)

After installation, you can use the CLI tool:

```bash
portfolio-tools --help
```

### Example CLI Usage

```bash
portfolio-tools -v
```
Shows the CLI version.

```bash
portfolio-tools composition -f portfolio.json
```
Plots the composition of the portfolio defined in the file `portfolio.json`.

```bash
portfolio-tools correlation -t AAPL,MSFT,GOOGL
```
Calculates the correlation between all pairs of the specified tickers.

```bash
portfolio-tools plot -t AAPL,MSFT,GOOGL
```
Plots the price evolution of the specified assets, showing their historical prices in a single chart.

```bash
portfolio-tools print-positions -f portfolio.json
```
Prints a table of current portfolio positions from the file `portfolio.json`.

```bash
portfolio-tools clear-cache
```
Deletes all cache files in the `temp/` directory (files ending with `.pkl`).

```bash
portfolio-tools ticker-info -t AAPL
```
Shows detailed information for a ticker in a formatted table.

### Local CLI Usage

```bash
python -m cli.cli -v
```

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

---

# Library Usage

## Main Modules

### Portfolio

The `Portfolio` class allows you to manage and analyze an investment portfolio.

#### Initialization

```python
from portfolio_tools.portfolio.portfolio import Portfolio
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider

# Create the data provider
data_provider = YFDataProvider()

# Load portfolio from JSON
portfolio = Portfolio(json_filepath="portfolio_example.json", data_provider=data_provider)
```

#### Visualization

```python
# Pie chart of current portfolio composition
df = portfolio.df_portfolio
from portfolio_tools.portfolio.plot import plot_composition, plot_evolution_ticker, plot_evolution_vs_cost, plot_evolution_stacked
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
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider

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
from portfolio_tools.utils.log_returns import calculate_log_returns
from portfolio_tools.utils.correlation import calculate_correlation

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

The JSON file to load a portfolio must have the following structure (Portfolio V2 format):

```json
{
  "name": "My Portfolio",
  "currency": "EUR",
  "transactions": [
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
    },
    {
      "ticker": "AAPL",
      "date": "2025-06-12",
      "type": "buy",
      "quantity": 10,
      "price": 100.00,
      "currency": "USD",
      "total": 1000.00,
      "exchange_rate": 1.056,
      "subtotal_base": 947.00,
      "fees_base": 0.50,
      "total_base": 947.50
    },
    {
      "ticker": "AAPL",
      "date": "2025-06-13",
      "type": "sell",
      "quantity": 5,
      "price": 110.00,
      "currency": "USD",
      "total": 550.00,
      "exchange_rate": 1.058,
      "subtotal_base": 519.85,
      "fees_base": 0.50,
      "total_base": 519.35
    },
    {
      "ticker": null,
      "date": "2025-06-20",
      "type": "withdrawal",
      "quantity": 200.00,
      "price": 1.00,
      "currency": "EUR",
      "total": 200.00,
      "exchange_rate": 1.00,
      "subtotal_base": 200.00,
      "fees_base": 5.00,
      "total_base": 205.00
    }
  ]
}
```

### Portfolio Structure Fields

- **`name`**: Portfolio name (string)
- **`currency`**: Base currency for the portfolio (e.g., "EUR", "USD", "CAD")
- **`transactions`**: Array of all transactions (deposits, withdrawals, buys, sells)

### Transaction Fields

Each transaction must include:

- **`ticker`**: Stock ticker symbol (e.g., "AAPL") or `null` for cash transactions
- **`date`**: Transaction date in "YYYY-MM-DD" format
- **`type`**: Transaction type: "buy", "sell", "deposit", "withdrawal"
- **`quantity`**: Number of shares (for stocks) or amount (for cash)
- **`price`**: Price per share (for stocks) or 1.00 (for cash)
- **`currency`**: Transaction currency (e.g., "USD", "EUR", "CAD")
- **`total`**: Total amount in transaction currency
- **`exchange_rate`**: Exchange rate from transaction currency to base currency
- **`subtotal_base`**: Subtotal in base currency (before fees)
- **`fees_base`**: Fees in base currency
- **`total_base`**: Total amount in base currency (including fees)

### Transaction Types

1. **Cash Transactions** (`ticker: null`):
   - `deposit`: Adding money to the portfolio
   - `withdrawal`: Removing money from the portfolio

2. **Stock Transactions** (`ticker: "SYMBOL"`):
   - `buy`: Purchasing shares
   - `sell`: Selling shares

### Multi-Currency Support

The system supports multiple currencies with automatic conversion:
- **Transaction currency**: The currency in which the transaction occurred
- **Base currency**: The portfolio's base currency for reporting
- **Exchange rate**: Used to convert transaction amounts to base currency
- **Automatic cash tracking**: The system automatically creates synthetic cash transactions for stock purchases/sales

### Migration from V1 Format

If you have portfolios in the old V1 format, use the migration script:

```bash
python migrate_v1_to_v2.py old_portfolio.json new_portfolio.json --add-cash
```

### Example Portfolios

See `tests/examples/` for various portfolio examples:
- `basic_portfolio.json`: Simple portfolio with basic transactions
- `multi_currency_portfolio.json`: Portfolio with USD, CAD, and EUR transactions
- `fifo_test_portfolio.json`: Complex FIFO cost calculation example
- `cash_only_portfolio.json`: Portfolio with only cash transactions

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
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from portfolio_tools.utils.log_returns import calculate_log_returns
from portfolio_tools.utils.correlation import calculate_correlation

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
from portfolio_tools.portfolio.plot import plot_composition
plot_composition(portfolio.df_portfolio, group_by="sector")
```

---

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
