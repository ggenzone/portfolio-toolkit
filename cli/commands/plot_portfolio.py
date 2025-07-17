import click
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from portfolio_tools.portfolio.portfolio import Portfolio


@click.command(name='plot-portfolio')
@click.option('-f', '--file', 'portfolio_file', required=True, 
              help='Portfolio file in JSON format')
def plot_portfolio(portfolio_file):
    """Plot the portfolio evolution."""
    try:
        # Initialize data provider
        data_provider = YFDataProvider()
        
        # Load portfolio
        portfolio = Portfolio(portfolio_file, data_provider)

        # Plot portfolio evolution
        portfolio.plot_evolution()
        
    except FileNotFoundError:
        print(f"Error: Portfolio file '{portfolio_file}' not found.")
    except Exception as e:
        print(f"Error loading portfolio: {e}")
