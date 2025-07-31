import click

from .dump_data_frame import dump_data_frame
from .evolution import evolution
from .performance import performance

# Import individual command modules
from .positions import positions
from .tax_report import tax_report
from .transactions import transactions


@click.group()
def portfolio():
    """Portfolio analysis commands"""
    pass


@portfolio.group()
def debug():
    """Debug portfolio data"""
    pass


portfolio.add_command(transactions)
portfolio.add_command(positions)

portfolio.add_command(evolution)
portfolio.add_command(performance)

portfolio.add_command(tax_report)

# Add debug commands
debug.add_command(dump_data_frame)
