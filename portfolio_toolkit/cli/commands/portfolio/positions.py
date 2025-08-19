import click

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.plot.engine import PlotEngine
from portfolio_toolkit.portfolio import Portfolio

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
    portfolio = Portfolio.from_dict(data, data_provider=data_provider)
    open_positions = portfolio.get_open_positions(date)

    # Aquí puedes usar los parámetros opcionales
    if output_file:
        click.echo(f"Output will be saved to: {output_file}")
        open_positions.to_dataframe().to_csv(output_file, index=False)
        click.echo(f"✅ Open positions saved to {output_file}")
        # print_open_positions_to_csv(open_positions, output_file)
    else:
        print(f"Open positions for {portfolio.name} on {date}:")
        print(open_positions.to_dataframe().to_string(index=False))

    if plot:
        group_by = "Ticker"
        if country:
            group_by = "Country"
        elif sector:
            group_by = "Sector"

        pie_data = open_positions.get_pie_chart_data(group_by=group_by)
        PlotEngine.plot(pie_data)
