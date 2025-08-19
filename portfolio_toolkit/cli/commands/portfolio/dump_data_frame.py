import click

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.portfolio import Portfolio

from ..utils import load_json_file


@click.command()
@click.argument("file", type=click.Path(exists=True))
def dump_data_frame(file):
    """Show portfolio data frame"""
    data = load_json_file(file)
    data_provider = YFDataProvider()
    basic_portfolio = Portfolio.from_dict(data, data_provider=data_provider)
    time_series = basic_portfolio.get_time_series()
    time_series.print()
