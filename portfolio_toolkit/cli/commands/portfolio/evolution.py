import click

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.plot.engine import PlotEngine
from portfolio_toolkit.portfolio import Portfolio

from ..utils import load_json_file


@click.command()
@click.argument("file", type=click.Path(exists=True))
def evolution(file):
    """Plot portfolio value evolution"""
    data = load_json_file(file)
    data_provider = YFDataProvider()
    basic_portfolio = Portfolio.from_dict(data, data_provider=data_provider)
    time_series = basic_portfolio.get_time_series()

    line_data = time_series.plot_evolution()
    PlotEngine.plot(line_data)
