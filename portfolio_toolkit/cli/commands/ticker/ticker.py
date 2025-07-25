import click
from pathlib import Path

# Import individual command modules
from .info import info
from .returns import returns
from .stats import stats
from .correlation import correlation
from .beta import beta
from .returns_distribution import returns_distribution
from .volatility import volatility
from .export_data import data
from .compare import compare
from .evolution import evolution


@click.group()
def ticker():
    """Ticker analysis commands"""
    pass


@ticker.group()
def print():
    """Print ticker information"""
    pass


@ticker.group()
def plot():
    """Plot ticker data"""
    pass


@ticker.group()
def export():
    """Export ticker data"""
    pass


# Add compare command directly to ticker group
ticker.add_command(compare)
ticker.add_command(correlation)
ticker.add_command(evolution)

# Add print commands
print.add_command(info)

print.add_command(stats)
# print.add_command(correlation)
print.add_command(beta)

# Add plot commands
plot.add_command(returns_distribution)
plot.add_command(volatility)

# Add export commands
export.add_command(data)
export.add_command(returns)
