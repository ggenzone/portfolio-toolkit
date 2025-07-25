import click

from ..utils import not_implemented


@click.command()
@click.argument("symbol")
def data(symbol):
    """Export historical ticker data"""
    not_implemented(f"ticker export data {symbol}")
