import click
from portfolio_tools.plot.engine import PlotEngine
from portfolio_tools.portfolio.portfolio import Portfolio
from portfolio_tools.position.print_open_positions import print_open_positions, print_open_positions_to_csv
from portfolio_tools.position.get_open_positions import get_open_positions
from portfolio_tools.position.plot_open_positions import plot_open_positions
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from ..utils import load_json_file


@click.command('open-positions')
@click.argument('file', type=click.Path(exists=True))
@click.argument('date', type=click.STRING) # click.DateTime(formats=["%Y-%m-%d"])
@click.option('-o', '--output', 'output_file', default=None, help='Output CSV file forma (optional)')
@click.option('--plot', is_flag=True, help='Plot open positions (optional)')
def open_positions(file, date, output_file, plot):
    """Show open positions"""
    data = load_json_file(file)
    data_provider = YFDataProvider()
    portfolio = Portfolio(json_filepath=file, data_provider=data_provider)
    open_positions = get_open_positions(portfolio.assets, date)



    # Aquí puedes usar los parámetros opcionales
    if output_file:
        click.echo(f"Output will be saved to: {output_file}")
        print_open_positions_to_csv(open_positions, output_file)
    else:
        print_open_positions(open_positions)

    if plot:
        pie_data = plot_open_positions(open_positions)
        PlotEngine.plot(pie_data)
