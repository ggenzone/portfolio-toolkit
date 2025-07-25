import click
from ..utils import not_implemented, load_json_file


@click.command()
@click.argument('file', type=click.Path(exists=True))
def rebalance(file):
    """Suggest rebalancing according to target allocation"""
    data = load_json_file(file)
    not_implemented("portfolio suggest rebalance")
