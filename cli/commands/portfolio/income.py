import click
from datetime import datetime

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
    from_date = portfolio.start_date.strftime('%Y-%m-%d')
    to_date = datetime.now().strftime('%Y-%m-%d')

    click.echo(f"📈 Income summary from {from_date} to {to_date} for portfolio: {portfolio.name}")
    print_cash_incomes(portfolio, from_date=from_date, to_date=to_date)

