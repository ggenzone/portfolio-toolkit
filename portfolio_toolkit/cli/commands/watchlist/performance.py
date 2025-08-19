import click

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.utils import get_last_periods
from portfolio_toolkit.watchlist import Watchlist
from portfolio_toolkit.watchlist.performance import performance as performance_w

from ..utils import load_json_file


@click.command("performance")
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "-n",
    "--periods",
    type=int,
    default=4,
    help="Number of periods to analyze (default: 4)",
)
@click.option(
    "--period-type",
    type=click.Choice(["weeks", "months", "quarters", "years"]),
    default="weeks",
    help="Type of period to analyze (default: weeks)",
)
@click.option(
    "--output",
    type=click.Path(),
    default=None,
    help="Save results to CSV file instead of printing to console",
)
def performance(file, periods, period_type, output):
    """Show performance summary of the portfolio across multiple periods"""
    data = load_json_file(file)

    data_provider = YFDataProvider()
    watchlist = Watchlist.from_dict(data, data_provider=data_provider)

    # Obtener los períodos especificados
    period_objects = get_last_periods(
        n=periods, period_type=period_type, include_current=True
    )

    # Mostrar información de períodos solo si no se guarda en archivo
    if not output:
        period_dates = ", ".join(
            p.end_date.strftime("%Y-%m-%d") for p in period_objects
        )
        print(f"Últimos {periods} {period_type}: {period_dates}")

    performance_df = performance_w(watchlist.assets, period_objects)

    # Guardar en archivo CSV o mostrar en consola
    if output:
        performance_df.to_csv(output)
        click.echo(f"✅ Resultados guardados en: {output}")
        click.echo(f"📊 Análisis de {periods} {period_type}")
    else:
        # Imprimir tabla en consola
        display_text = "Rendimiento"
        period_text = period_type.capitalize()

        click.echo(f"\n📊 {display_text} por {period_text}")
        click.echo("=" * 60)
        click.echo(performance_df.to_string())

        click.echo("\nNota: Porcentajes de rendimiento vs período anterior")
