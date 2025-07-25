import click

from ..utils import load_json_file, not_implemented


@click.command("cumulative-returns")
@click.argument("file", type=click.Path(exists=True))
def cumulative_returns(file):
    """Plot cumulative returns"""
    data = load_json_file(file)
    not_implemented("portfolio plot cumulative-returns")
