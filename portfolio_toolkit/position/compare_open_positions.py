from typing import List

import pandas as pd

from portfolio_toolkit.portfolio.portfolio import Portfolio
from portfolio_toolkit.utils.period import Period


def _calculate_asset_values_for_display(
    asset: str, periods: List[Period], period_positions: dict
) -> List[str]:
    """
    Calculate asset values for 'value' display mode.

    Args:
        asset: Asset ticker
        periods: List of periods
        period_positions: Dictionary mapping period labels to position dictionaries

    Returns:
        List of formatted values or "-" for missing positions
    """
    asset_values = []
    for period in periods:
        if asset in period_positions[period.label]:
            position = period_positions[period.label][asset]
            asset_values.append(f"{position.value:.2f} ({position.quantity})")
        else:
            asset_values.append("-")
    return asset_values


def _calculate_asset_returns_for_display(
    asset: str, periods: List[Period], period_positions: dict
) -> List[str]:
    """
    Calculate asset returns based on price movement using buy_price and current_price.
    This avoids confusion from additional purchases or partial sales.

    Args:
        asset: Asset ticker
        periods: List of periods
        period_positions: Dictionary mapping period labels to position dictionaries

    Returns:
        List of formatted percentage returns or "-" for missing/first period
    """
    asset_values = []
    for i, period in enumerate(periods):
        if i == 0:
            # First period: always "-" (will be removed later if needed)
            asset_values.append("-")
        else:
            prev_period = periods[i - 1]
            current_period = period

            # Case 1: Asset exists in both periods - use current_price movement
            if (
                asset in period_positions[prev_period.label]
                and asset in period_positions[current_period.label]
            ):

                prev_position = period_positions[prev_period.label][asset]
                current_position = period_positions[current_period.label][asset]

                prev_price = prev_position.current_price
                current_price = current_position.current_price

                if prev_price > 0:
                    return_pct = ((current_price - prev_price) / prev_price) * 100
                    asset_values.append(f"{return_pct:.2f}%")
                else:
                    asset_values.append("-")

            # Case 2: New position - return from buy_price to current_price
            elif (
                asset not in period_positions[prev_period.label]
                and asset in period_positions[current_period.label]
            ):

                position = period_positions[current_period.label][asset]
                buy_price = position.buy_price
                current_price = position.current_price

                if buy_price > 0:
                    return_pct = ((current_price - buy_price) / buy_price) * 100
                    asset_values.append(f"{return_pct:.2f}%")
                else:
                    asset_values.append("-")

            # Case 3: Position sold (existed before, doesn't exist now)
            elif (
                asset in period_positions[prev_period.label]
                and asset not in period_positions[current_period.label]
            ):
                asset_values.append("SOLD")

            # Case 4: Doesn't exist in either period
            else:
                asset_values.append("-")

    return asset_values


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
        positions = portfolio.get_open_positions(end_date_str)
        period_positions[period.label] = {pos.ticker: pos for pos in positions}
        all_assets.update(pos.ticker for pos in positions)

    # Create comparison data
    comparison_data = {}

    for asset in sorted(all_assets):
        if display == "value":
            asset_values = _calculate_asset_values_for_display(
                asset, periods, period_positions
            )
        elif display == "return":
            asset_values = _calculate_asset_returns_for_display(
                asset, periods, period_positions
            )

        comparison_data[asset] = asset_values

    # Add CASH row
    cash_values = []
    for i, period in enumerate(periods):
        cash_amount = portfolio.account.get_amount_at(period.end_date)

        if display == "value":
            cash_values.append(f"{cash_amount:.2f}")
        elif display == "return":
            if i == 0:
                cash_values.append("-")
            else:
                prev_period = periods[i - 1]
                prev_cash = portfolio.account.get_amount_at(prev_period.end_date)
                if prev_cash > 0:
                    cash_return = ((cash_amount - prev_cash) / prev_cash) * 100
                    cash_values.append(f"{cash_return:.2f}%")
                else:
                    cash_values.append("-")

    comparison_data["CASH"] = cash_values

    # Add TOTAL row (portfolio value + cash)
    total_values = []
    for i, period in enumerate(periods):
        # Calculate total portfolio value (positions + cash)
        portfolio_value = 0
        for asset in all_assets:
            if asset in period_positions[period.label]:
                portfolio_value += period_positions[period.label][asset].value

        cash_amount = portfolio.account.get_amount_at(period.end_date)
        total_value = portfolio_value + cash_amount

        if display == "value":
            total_values.append(f"{total_value:.2f}")
        elif display == "return":
            if i == 0:
                total_values.append("-")
            else:
                prev_period = periods[i - 1]
                # Calculate previous total
                prev_portfolio_value = 0
                for asset in all_assets:
                    if asset in period_positions[prev_period.label]:
                        prev_portfolio_value += period_positions[prev_period.label][
                            asset
                        ].value

                prev_cash = portfolio.account.get_amount_at(prev_period.end_date)
                prev_total = prev_portfolio_value + prev_cash

                if prev_total > 0:
                    total_return = ((total_value - prev_total) / prev_total) * 100
                    total_values.append(f"{total_return:.2f}%")
                else:
                    total_values.append("-")

    comparison_data["TOTAL"] = total_values

    # Create DataFrame
    period_labels = [period.label for period in periods]
    df = pd.DataFrame(comparison_data, index=period_labels).T

    return df
