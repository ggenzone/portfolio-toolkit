import click

from ..utils import not_implemented


@click.command("returns-distribution")
@click.argument("symbol")
def returns_distribution(symbol):
    """Plot daily returns distribution"""
    not_implemented(f"ticker plot returns-distribution {symbol}")
