import click
from portfolio_tools.plot.engine import PlotEngine
from portfolio_tools.portfolio.load_portfolio_json import load_portfolio_json
from portfolio_tools.position.get_open_positions import get_open_positions
from portfolio_tools.position.plot_open_positions import plot_open_positions
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from ..utils import load_json_file


@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.argument('date', type=click.STRING) # click.DateTime(formats=["%Y-%m-%d"])
@click.option('--country', is_flag=True, help='Plot open positions by country (optional)')
def allocation(file, date, country):
    """Plot current portfolio allocation"""
    data = load_json_file(file)
    data_provider = YFDataProvider()
    portfolio = load_portfolio_json(file, data_provider)
    open_positions = get_open_positions(portfolio.assets, date)

    pie_data = plot_open_positions(open_positions, group_by='Country' if country else 'Sector')
    PlotEngine.plot(pie_data)
