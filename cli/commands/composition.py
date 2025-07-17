import click
from portfolio_tools.portfolio.portfolio import Portfolio
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider


@click.command()
@click.option('-f', '--file', 'portfolio_file', required=True, 
              help='Portfolio file in JSON format')
def composition(portfolio_file):
    """Plot the portfolio composition."""
    data_provider = YFDataProvider()
    cartera = Portfolio(json_filepath=portfolio_file, data_provider=data_provider)
    cartera.plot_composition()
