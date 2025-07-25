import click
from portfolio_toolkit.portfolio.load_portfolio_json import load_portfolio_json
from portfolio_toolkit.asset.print import print_asset_transactions_csv
from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from ..utils import load_json_file


@click.command()
@click.argument('file', type=click.Path(exists=True))
def transactions(file):
    """Show portfolio transactions"""
    data = load_json_file(file)
    data_provider = YFDataProvider()
    portfolio = load_portfolio_json(json_filepath=file, data_provider=data_provider)

    print_asset_transactions_csv(portfolio.assets)
