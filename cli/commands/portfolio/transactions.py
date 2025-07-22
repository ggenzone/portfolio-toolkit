import click
from portfolio_tools.portfolio.portfolio import Portfolio
from portfolio_tools.asset.print import print_asset_transactions_csv
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from ..utils import load_json_file


@click.command()
@click.argument('file', type=click.Path(exists=True))
def transactions(file):
    """Show portfolio transactions"""
    data = load_json_file(file)
    data_provider = YFDataProvider()
    portfolio = Portfolio(json_filepath=file, data_provider=data_provider)

    print_asset_transactions_csv(portfolio.assets)
