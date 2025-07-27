from typing import List

import pandas as pd

from portfolio_toolkit.portfolio.portfolio import Portfolio
from portfolio_toolkit.utils.period import Period

from .get_open_positions import get_open_positions


def compare_open_positions(
    portfolio: Portfolio, periods: List[Period], display="value"
) -> pd.DataFrame:
    """
    Compare open positions across multiple periods.

    Creates a DataFrame showing position values or returns at the end of each period.
    Rows represent assets, columns represent periods.

    Args:
        portfolio: Portfolio object containing assets
        periods: List of Period objects to compare
        display: 'value' shows position values, 'return' shows percentage returns

    Returns:
        pd.DataFrame: DataFrame with assets as rows and periods as columns.
                     For 'value': Values show position market value, "-" for missing positions.
                     For 'return': Values show percentage return vs previous period, "-" for missing/first period.

    Example:
        # Show values
        df = compare_open_positions(portfolio, periods, display='value')
        Result:
                    Q1 2025    Q2 2025
        AAPL        1500.00    1650.00
        GOOGL       2000.00    -

        # Show returns
        df = compare_open_positions(portfolio, periods, display='return')
        Result:
                    Q1 2025    Q2 2025
        AAPL        -          10.00%
        GOOGL       -          -
    """
    if display not in ["value", "return"]:
        raise ValueError("display must be 'value' or 'return'")

    # Get positions for each period end date
    period_positions = {}
    all_assets = set()

    for period in periods:
        end_date_str = period.end_date.strftime("%Y-%m-%d")
        positions = get_open_positions(portfolio.assets, end_date_str)
        period_positions[period.label] = {pos.ticker: pos for pos in positions}
        all_assets.update(pos.ticker for pos in positions)

    # Create comparison data
    comparison_data = {}

    for asset in sorted(all_assets):
        if display == "value":
            asset_values = []
            for period in periods:
                if asset in period_positions[period.label]:
                    position = period_positions[period.label][asset]
                    asset_values.append(f"{position.value:.2f}")
                else:
                    asset_values.append("-")

        elif display == "return":
            asset_values = []
            for i, period in enumerate(periods):
                if i == 0:
                    # First period has no comparison
                    asset_values.append("-")
                else:
                    prev_period = periods[i - 1]
                    current_period = period

                    # Check if asset exists in both periods
                    if (
                        asset in period_positions[prev_period.label]
                        and asset in period_positions[current_period.label]
                    ):

                        prev_value = period_positions[prev_period.label][asset].value
                        current_value = period_positions[current_period.label][
                            asset
                        ].value

                        if prev_value > 0:
                            return_pct = (
                                (current_value - prev_value) / prev_value
                            ) * 100
                            asset_values.append(f"{return_pct:.2f}%")
                        else:
                            asset_values.append("-")
                    else:
                        asset_values.append("-")

        comparison_data[asset] = asset_values

    # Create DataFrame
    period_labels = [period.label for period in periods]
    df = pd.DataFrame(comparison_data, index=period_labels).T

    return df
