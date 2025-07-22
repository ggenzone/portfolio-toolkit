import click
from ..utils import not_implemented, load_json_file


@click.command()
@click.argument('file', type=click.Path(exists=True))
def income(file):
    """Show income summary (dividends, etc.)"""
    data = load_json_file(file)
    not_implemented("portfolio print income")
