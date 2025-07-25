import click

from ..utils import not_implemented


@click.command()
@click.argument("symbols", nargs=-1, required=True)
def compare(symbols):
    """Compare multiple tickers"""
    if len(symbols) < 2:
        click.echo("Error: At least 2 symbols are required")
        return
    not_implemented(f"ticker compare {' '.join(symbols)}")
