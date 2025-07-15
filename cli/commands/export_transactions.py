from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from portfolio_tools.portfolio.portfolio import Portfolio


def run(args):
    """
    Exports all portfolio transactions in CSV format, ordered by date.
    
    Args:
        args: Command line arguments containing the portfolio file path.
    """
    try:
        # Initialize data provider
        data_provider = YFDataProvider()
        
        # Load portfolio
        portfolio = Portfolio(args.file, data_provider)
        
        # Export transactions in CSV format
        portfolio.print_transactions()
        
    except FileNotFoundError:
        print(f"Error: Portfolio file '{args.file}' not found.")
    except Exception as e:
        print(f"Error loading portfolio: {e}")
