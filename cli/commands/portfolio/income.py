import click
from portfolio_tools.portfolio.load_portfolio_json import load_portfolio_json
from portfolio_tools.portfolio.print_cash_incomes import print_cash_incomes
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from ..utils import load_json_file


@click.command()
@click.argument('file', type=click.Path(exists=True))
def income(file):
    """Show income summary (dividends, etc.)"""
    data = load_json_file(file)
    data_provider = YFDataProvider()
    portfolio = load_portfolio_json(json_filepath=file, data_provider=data_provider)
    print_cash_incomes(portfolio)



