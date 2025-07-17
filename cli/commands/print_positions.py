import click
from portfolio_tools.portfolio.portfolio import Portfolio
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider


@click.command(name='print-positions')
@click.option('-f', '--file', 'portfolio_file', required=True, 
              help='Portfolio file in JSON format')
@click.option('-d', '--date', help='Target date in YYYY-MM-DD format (optional)')
def print_positions(portfolio_file, date):
    """Print current portfolio positions as a table."""
    data_provider = YFDataProvider()
    portfolio = Portfolio(json_filepath=portfolio_file, data_provider=data_provider)
    portfolio.print_current_positions(date)
