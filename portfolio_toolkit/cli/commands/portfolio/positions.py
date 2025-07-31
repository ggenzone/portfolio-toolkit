import click

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.plot.engine import PlotEngine
from portfolio_toolkit.portfolio.load_portfolio_json import load_portfolio_json
from portfolio_toolkit.position.get_open_positions import get_open_positions
from portfolio_toolkit.position.plot_open_positions import plot_open_positions
from portfolio_toolkit.position.print_open_positions import print_open_positions
from portfolio_toolkit.position.valued_position import ValuedPosition

from ..utils import load_json_file


@click.command("positions")
@click.argument("file", type=click.Path(exists=True))
@click.argument("date", type=click.STRING)  # click.DateTime(formats=["%Y-%m-%d"])
@click.option(
    "-o",
    "--output",
    "output_file",
    default=None,
    help="Output CSV file forma (optional)",
)
@click.option("--plot", is_flag=True, help="Plot open positions (optional)")
@click.option(
    "--country", is_flag=True, help="Plot open positions by country (optional)"
)
@click.option("--sector", is_flag=True, help="Plot open positions by sector (optional)")
def positions(file, date, output_file, plot, country, sector):
    """Show open positions"""
    data = load_json_file(file)
    data_provider = YFDataProvider()
    portfolio = load_portfolio_json(data, data_provider=data_provider)
    open_positions = get_open_positions(portfolio.assets, date)

    # Aquí puedes usar los parámetros opcionales
    if output_file:
        click.echo(f"Output will be saved to: {output_file}")
        ValuedPosition.to_dataframe(open_positions).to_csv(output_file)
        click.echo(f"✅ Open positions saved to {output_file}")
        # print_open_positions_to_csv(open_positions, output_file)
    else:
        print_open_positions(open_positions)

    if plot:
        group_by = "Ticker"
        if country:
            group_by = "Country"
        elif sector:
            group_by = "Sector"

        pie_data = plot_open_positions(open_positions, group_by=group_by)
        PlotEngine.plot(pie_data)
