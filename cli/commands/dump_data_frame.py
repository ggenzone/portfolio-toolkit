import click
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from portfolio_tools.portfolio.portfolio import Portfolio


@click.command(name='dump-data-frame')
@click.option('-f', '--file', 'portfolio_file', required=True, 
              help='Portfolio file in JSON format')
def dump_data_frame(portfolio_file):
    """Dump portfolio DataFrame for debugging purposes."""
    try:
        # Initialize data provider
        data_provider = YFDataProvider()
        
        # Load portfolio
        portfolio = Portfolio(portfolio_file, data_provider)
        
        # The DataFrame is already printed during initialization
        # But we can call it explicitly for clarity
        print("\n" + "="*80)
        print("PORTFOLIO DATAFRAME DUMP")
        print("="*80)
        portfolio.print_data_frame()
        
    except FileNotFoundError:
        print(f"Error: Portfolio file '{portfolio_file}' not found.")
    except Exception as e:
        print(f"Error loading portfolio: {e}")
        print(e.with_traceback())
