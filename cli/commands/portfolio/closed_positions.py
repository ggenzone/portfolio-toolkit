import click
from portfolio_tools.portfolio.load_portfolio_json import load_portfolio_json
from portfolio_tools.position.print_closed_positions import print_closed_positions, print_closed_positions_to_csv, print_closed_positions_summary
from portfolio_tools.position.get_closed_positions import get_closed_positions
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from portfolio_tools.position.plot_closed_positions import plot_closed_positions
from portfolio_tools.plot.engine import PlotEngine
from ..utils import load_json_file


@click.command('closed-positions')
@click.argument('file', type=click.Path(exists=True))
@click.argument('date', type=click.STRING) # click.DateTime(formats=["%Y-%m-%d"])
@click.option('-o', '--output', 'output_file', default=None, help='Output CSV file forma (optional)')
@click.option('--plot', is_flag=True, help='Plot closed positions (optional)')
def closed_positions(file, date, output_file, plot):
    """Show closed positions"""
    data = load_json_file(file)
    data_provider = YFDataProvider()
    portfolio = load_portfolio_json(json_filepath=file, data_provider=data_provider)

    closed_positions = get_closed_positions(portfolio.assets, from_date='2010-01-01', to_date=date)
        
    # Aquí puedes usar los parámetros opcionales
    if output_file:
        click.echo(f"Output will be saved to: {output_file}")
        print_closed_positions_to_csv(closed_positions, date, output_file)
        print_closed_positions_summary(closed_positions, date)
    else:
        print_closed_positions(closed_positions, date)
        print_closed_positions_summary(closed_positions, date)
    
    if plot:
        bar_data = plot_closed_positions(closed_positions)
        PlotEngine.plot(bar_data)
