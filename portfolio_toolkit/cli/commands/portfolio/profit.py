import click

from ..utils import load_json_file, not_implemented


@click.command()
@click.argument("file", type=click.Path(exists=True))
def profit(file):
    """Plot profit by position"""
    data = load_json_file(file)
    not_implemented("portfolio plot profit")
