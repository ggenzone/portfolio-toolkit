from portfolio_toolkit.account.account import Account
from portfolio_toolkit.position import get_closed_positions_stats, get_valuation
from portfolio_toolkit.position.closed_position import ClosedPosition
from portfolio_toolkit.position.get_closed_positions import get_closed_positions
from portfolio_toolkit.position.get_open_positions import get_open_positions
from portfolio_toolkit.position.valued_position import ValuedPosition

from .portfolio import Portfolio
from .portfolio_stats import PortfolioStats


def get_portfolio_stats(portfolio: Portfolio, year: str) -> PortfolioStats:
    """
    Calculate comprehensive portfolio statistics for a given year.

    Args:
        portfolio (Portfolio): Portfolio object to analyze
        year (str): Year for which to calculate statistics

    Returns:
        PortfolioStats: Dataclass containing all portfolio metrics and data
    """
    previous_year = int(year) - 1
    previous_last_day = f"{previous_year}-12-31"

    first_day = f"{year}-01-01"
    last_day = f"{year}-12-31"

    # Get positions
    last_open_positions = get_open_positions(portfolio.assets, previous_last_day)
    open_positions = get_open_positions(portfolio.assets, last_day)
    closed_positions = get_closed_positions(
        portfolio.assets, from_date=first_day, to_date=last_day
    )

    # Convert to DataFrames
    closed_positions_df = ClosedPosition.to_dataframe(closed_positions)
    open_positions_df = ValuedPosition.to_dataframe(open_positions)
    transactions_df = Account.export_to_dataframe(
        portfolio.account, from_date=first_day, to_date=last_day
    )

    # Get detailed statistics
    closed_positions_stats = get_closed_positions_stats(closed_positions, last_day)

    # Calculate financial metrics
    realized_profit = closed_positions_stats["total_profit"]
    open_positions_cost = sum(pos.cost for pos in open_positions)
    open_positions_valuation = get_valuation(open_positions)

    # Create and return PortfolioStats dataclass
    return PortfolioStats(
        realized_profit=realized_profit,
        unrealized_profit=open_positions_valuation - open_positions_cost,
        initial_valuation=get_valuation(last_open_positions),
        final_valuation=open_positions_valuation,
        incomes=transactions_df[transactions_df["type"] == "income"]["amount"].sum(),
        deposits=transactions_df[transactions_df["type"] == "deposit"]["amount"].sum(),
        withdrawals=transactions_df[transactions_df["type"] == "withdrawal"][
            "amount"
        ].sum(),
        commission=0.0,
        closed_positions_stats=closed_positions_stats,
        closed_positions=closed_positions_df,
        open_positions=open_positions_df,
        transactions=transactions_df,
    )
