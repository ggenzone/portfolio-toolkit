import click

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.portfolio.load_portfolio_json import load_portfolio_json
from portfolio_toolkit.portfolio.print_date_frame import print_data_frame
from portfolio_toolkit.portfolio.time_series_portfolio import (
    create_time_series_portfolio_from_portfolio,
)

from ..utils import load_json_file


@click.command()
@click.argument("file", type=click.Path(exists=True))
def dump_data_frame(file):
    """Show portfolio data frame"""
    data = load_json_file(file)
    data_provider = YFDataProvider()
    basic_portfolio = load_portfolio_json(
        json_filepath=file, data_provider=data_provider
    )
    portfolio = create_time_series_portfolio_from_portfolio(basic_portfolio)

    print_data_frame(portfolio)
