from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from portfolio_tools.portfolio.portfolio import Portfolio


def run(args):
    """
    Dumps the portfolio DataFrame for debugging purposes.
    
    Args:
        args: Command line arguments containing the portfolio file path.
    """
    try:
        # Initialize data provider
        data_provider = YFDataProvider()
        
        # Load portfolio
        portfolio = Portfolio(args.file, data_provider)
        
        # The DataFrame is already printed during initialization
        # But we can call it explicitly for clarity
        print("\n" + "="*80)
        print("PORTFOLIO DATAFRAME DUMP")
        print("="*80)
        portfolio.print_data_frame()
        
    except FileNotFoundError:
        print(f"Error: Portfolio file '{args.file}' not found.")
    except Exception as e:
        print(f"Error loading portfolio: {e}")
