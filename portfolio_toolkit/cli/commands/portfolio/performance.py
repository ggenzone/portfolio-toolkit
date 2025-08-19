import click

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.portfolio import Portfolio
from portfolio_toolkit.position.compare_open_positions import compare_open_positions
from portfolio_toolkit.utils import get_last_periods

from ..utils import load_json_file


@click.command("performance")
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "--display",
    type=click.Choice(["return", "value"]),
    default="return",
    help="Display mode: 'return' shows percentage returns, 'value' shows position values",
)
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
def performance(file, display, periods, period_type, output):
    """Show performance summary of the portfolio across multiple periods"""
    data = load_json_file(file)

    data_provider = YFDataProvider()
    portfolio = Portfolio.from_dict(data, data_provider=data_provider)

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

    # Obtener comparación de posiciones
    positions_df = compare_open_positions(portfolio, period_objects, display=display)

    # Guardar en archivo CSV o mostrar en consola
    if output:
        positions_df.to_csv(output)
        click.echo(f"✅ Resultados guardados en: {output}")
        click.echo(f"📊 Análisis de {periods} {period_type} - Modo: {display}")
    else:
        # Imprimir tabla en consola
        display_text = "Rendimiento" if display == "return" else "Valores"
        period_text = period_type.capitalize()

        click.echo(f"\n📊 {display_text} por {period_text}")
        click.echo("=" * 60)
        click.echo(positions_df.to_string())

        if display == "return":
            click.echo("\nNota: Porcentajes de rendimiento vs período anterior")
        else:
            click.echo(
                f"\nNota: Valores de posiciones al final de cada {period_type[:-1]}"
            )
