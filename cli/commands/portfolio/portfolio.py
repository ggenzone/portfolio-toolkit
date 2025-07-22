import click
from pathlib import Path

# Import individual command modules
from .open_positions import open_positions
from .closed_positions import closed_positions
from .performance_summary import performance_summary
from .income import income
from .evolution import evolution
from .cumulative_returns import cumulative_returns
from .profit import profit
from .allocation import allocation
from .rebalance import rebalance
from .tax_report import tax_report
from .transactions import transactions
from .dump_data_frame import dump_data_frame


@click.group()
def portfolio():
    """Portfolio analysis commands"""
    pass


@portfolio.group()
def print():
    """Print portfolio information"""
    pass


@portfolio.group()
def plot():
    """Plot portfolio data"""
    pass


@portfolio.group()
def suggest():
    """Portfolio suggestions"""
    pass


@portfolio.group()
def export():
    """Export portfolio data"""
    pass

portfolio.add_command(open_positions)
portfolio.add_command(closed_positions)

# Add print commands
print.add_command(performance_summary)
print.add_command(income)
print.add_command(transactions)
print.add_command(dump_data_frame)

# Add plot commands
plot.add_command(evolution)
plot.add_command(cumulative_returns)
plot.add_command(profit)
plot.add_command(allocation)

# Add suggest commands
suggest.add_command(rebalance)

# Add export commands
export.add_command(tax_report)
