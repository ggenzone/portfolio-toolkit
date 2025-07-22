import click
from ..utils import not_implemented, load_json_file


@click.command('performance-summary')
@click.argument('file', type=click.Path(exists=True))
def performance_summary(file):
    """Show performance summary (CAGR, drawdown, Sharpe)"""
    data = load_json_file(file)
    not_implemented("portfolio print performance-summary")
