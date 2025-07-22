import click
from ..utils import not_implemented, load_json_file


@click.command('cumulative-returns')
@click.argument('file', type=click.Path(exists=True))
def cumulative_returns(file):
    """Plot cumulative returns"""
    data = load_json_file(file)
    not_implemented("portfolio plot cumulative-returns")
