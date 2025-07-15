# Portfolio Test Examples

This directory contains various portfolio examples to test different scenarios and use cases of the portfolio tools system.

## Available Examples

### 1. `basic_portfolio.json`
**Purpose**: Simple portfolio with basic stock transactions
- **Assets**: AAPL (Apple Inc.)
- **Currency**: EUR
- **Scenario**: Basic buy operation with EUR cash deposit
- **Features**: Single asset, EUR base currency, simple transactions

### 2. `multi_currency_portfolio.json` 
**Purpose**: Portfolio with transactions in multiple currencies
- **Assets**: AAPL (USD), SHOP (CAD)
- **Currency**: EUR (base)
- **Scenario**: Multi-currency trading with currency conversion
- **Features**: USD and CAD transactions converted to EUR, realistic exchange rates

### 3. `fifo_test_portfolio.json`
**Purpose**: Test FIFO (First In, First Out) cost calculation
- **Assets**: AAPL (Apple Inc.)
- **Currency**: EUR
- **Scenario**: Multiple buy operations followed by partial sell
- **Features**: Complex FIFO cost tracking, multiple buy/sell transactions

### 4. `cash_only_portfolio.json`
**Purpose**: Portfolio with only cash transactions (no stocks)
- **Assets**: Cash only (__EUR synthetic ticker)
- **Currency**: EUR
- **Scenario**: Deposits, withdrawals, and fees handling
- **Features**: Pure cash management, fee calculations

### 5. `test_portfolio_v2.json`
**Purpose**: Main test portfolio used for comprehensive testing
- **Assets**: AAPL (Apple Inc.)
- **Currency**: EUR
- **Scenario**: Complex operations with cash deposits and stock purchases
- **Features**: Complete portfolio lifecycle testing

## Using the Examples

### Running Individual Tests
```bash
# Test a specific portfolio
python3 -c "
from portfolio_tools.portfolio.portfolio import Portfolio
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider

data_provider = YFDataProvider()
portfolio = Portfolio('tests/examples/basic_portfolio.json', data_provider)
portfolio.print_current_positions()
"
```

### Validate All Examples
```bash
# Run comprehensive validation
python3 tests/validate_examples.py
```

### Run Unit Tests
```bash
# Run all portfolio tests
python3 -m pytest tests/test_portfolio_v2.py -v
```

## Portfolio V2 Format

All examples use the Portfolio V2 format which features:

- **Flat transaction structure**: All transactions in a single array
- **Synthetic cash tickers**: Cash represented as __EUR, __USD, etc.
- **Complete transaction details**: Each transaction includes:
  - `ticker`: Asset symbol (null for cash)
  - `date`: Transaction date
  - `type`: buy, sell, deposit, withdrawal
  - `quantity`: Number of shares/units
  - `price`: Price per unit in original currency
  - `currency`: Transaction currency
  - `total`: Total amount in original currency
  - `exchange_rate`: Conversion rate to base currency
  - `subtotal_base`: Amount in base currency before fees
  - `fees_base`: Fees in base currency
  - `total_base`: Total cost including fees in base currency

## Key Features Tested

### Currency Conversion
- Realistic exchange rates (EUR/USD: 1.05, EUR/CAD: 0.64)
- Multi-currency support
- Automatic conversion to base currency

### FIFO Cost Calculation
- First In, First Out cost basis tracking
- Accurate cost calculation for partial sales
- Fee inclusion in cost basis

### Fee Handling
- Transaction fees absorbed into pricing
- Proper fee allocation in multi-currency scenarios
- Fee impact on returns calculation

### Cash Management
- Synthetic cash tickers for different currencies
- Deposit and withdrawal tracking
- Cash balance calculations

## Testing Structure

The examples are designed to test:

1. **Basic Functionality**: Simple portfolio operations
2. **Multi-Currency Support**: Currency conversion and tracking
3. **Complex Calculations**: FIFO costing and fee handling
4. **Edge Cases**: Cash-only portfolios and withdrawals
5. **Integration**: Complete system workflow testing

Each example is self-contained and can be used independently for testing specific features or scenarios.
