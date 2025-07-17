import click
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from portfolio_tools.portfolio.portfolio import Portfolio


@click.command(name='export-transactions')
@click.option('-f', '--file', 'portfolio_file', required=True, 
              help='Portfolio file in JSON format')
def export_transactions(portfolio_file):
    """Export all portfolio transactions in CSV format."""
    try:
        # Initialize data provider
        data_provider = YFDataProvider()
        
        # Load portfolio
        portfolio = Portfolio(portfolio_file, data_provider)
        
        # Export transactions in CSV format
        portfolio.print_transactions()
        
    except FileNotFoundError:
        print(f"Error: Portfolio file '{portfolio_file}' not found.")
    except Exception as e:
        print(f"Error loading portfolio: {e}")
