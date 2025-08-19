[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/ggenzone/portfolio-toolkit/blob/master/README.md)
[![es](https://img.shields.io/badge/lang-es-green.svg)](https://github.com/ggenzone/portfolio-toolkit/blob/master/README.es.md)


# Portfolio-tools Library Documentation

![Documentation](https://img.shields.io/badge/docs-sphinx-brightgreen.svg)
![Tests](https://github.com/ggenzone/portfolio-toolkit/workflows/Tests%20and%20Quality%20Checks/badge.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)

This library provides tools for financial analysis, portfolio management, and market data visualization with comprehensive multi-currency support and FIFO cost calculation.

## 📚 Documentation

**[📖 Full Documentation](https://ggenzone.github.io/portfolio-toolkit/)** - Complete API reference, user guides, and examples

### Quick Documentation Links

- **[Getting Started](https://ggenzone.github.io/portfolio-toolkit/examples/basic_usage.html)** - Basic usage examples
- **[CLI Usage Guide](https://ggenzone.github.io/portfolio-toolkit/examples/cli_usage.html)** - Complete command-line interface reference
- **[Multi-Currency Support](https://ggenzone.github.io/portfolio-toolkit/examples/multi_currency.html)** - Working with multiple currencies
- **[Portfolio JSON Format](https://ggenzone.github.io/portfolio-toolkit/user_guide/portfolio_format.html)** - Complete format specification
- **[API Reference](https://ggenzone.github.io/portfolio-toolkit/api/modules.html)** - Full API documentation

### Building Documentation Locally

```bash
# Install documentation dependencies
pip install sphinx sphinx-rtd-theme

# Build documentation
./manage_docs.sh build

# Serve documentation locally
./manage_docs.sh serve

# Auto-rebuild on changes
./manage_docs.sh watch
```

## Code Quality

This project maintains high code quality standards using:

- **Black** - Code formatting
- **isort** - Import sorting  
- **flake8** - Linting
- **pytest** - Testing

### Quick Quality Checks

```bash
# Run all quality checks
./check_quality.sh

# Auto-format code
./format_code.sh

# Individual tools
black portfolio_toolkit/      # Format code
isort portfolio_toolkit/      # Sort imports
flake8 portfolio_toolkit/     # Lint code
pytest tests/              # Run tests
```

### Configuration

Code quality tools are configured in `pyproject.toml` and `setup.cfg`:
- Line length: 88 characters
- Black and isort profiles: compatible
- flake8 ignores: E203, E501, W503

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
pip uninstall portfolio-toolkit
```

## Testing

### Running Tests

```bash
# Run all tests and checks
./run_tests.sh

# Run specific test suites
./run_tests.sh unit         # Unit tests only
./run_tests.sh coverage     # Tests with coverage report
./run_tests.sh examples     # Validate example portfolios
./run_tests.sh cli          # Test CLI commands
./run_tests.sh lint         # Code quality checks
```

### Manual Testing

```bash
# Run unit tests directly
python -m pytest tests/ -v

# Validate example portfolios
python tests/validate_examples.py

# Test CLI commands
portfolio-tools print-positions -f tests/examples/basic_portfolio.json

# Or using the module directly
python -m portfolio_toolkit.cli.cli portfolio print performance-summary tests/examples/basic_portfolio.json

```

## Documentation

```bash
# Local development
./manage_docs.sh build      # Build documentation
./manage_docs.sh serve      # Serve locally
./manage_docs.sh watch      # Auto-rebuild on changes

# Deploy
./manage_docs.sh deploy     # Deploy to GitHub Pages
```

## To Do

- [x] Add unit and integration tests for all modules
- [x] Document all public methods with usage examples
- [x] Support multi-currency portfolios and automatic currency conversion
- [ ] Add support for more data providers (e.g., Alpha Vantage, IEX Cloud)
- [ ] Allow loading portfolios from Excel and ODS files natively
- [ ] Implement portfolio performance metrics (Sharpe, Sortino, drawdown, etc.)
- [ ] Add interactive visualizations (e.g., with Plotly or Dash)
- [ ] Document all public methods with usage examples
- [ ] Add export to PDF/Excel reports
- [ ] Allow portfolio rebalancing and optimization simulations
- [ ] Add risk analysis and Value at Risk (VaR)
- [x] Improve CLI interface for task automation (migrated to Click framework)
