from typing import List

from .get_current_month import get_current_month
from .get_current_quarter import get_current_quarter
from .get_current_week import get_current_week
from .get_current_year import get_current_year
from .get_last_months import get_last_months
from .get_last_quarters import get_last_quarters
from .get_last_weeks import get_last_weeks
from .get_last_years import get_last_years
from .period import Period


def get_last_periods(n=4, period_type="weeks", include_current=False) -> List[Period]:
    """
    Returns the last n periods as Period objects.

    Args:
        n (int): Number of periods to return
        period_type (str): Type of period ('years', 'quarters', 'months', 'weeks')
        include_current (bool): Whether to include the current period

    Returns:
        List[Period]: List of Period objects representing each period

    Example:
        # Get last 3 completed weeks
        get_last_periods(3, 'weeks', include_current=False)

        # Get last 2 weeks + current week
        get_last_periods(2, 'weeks', include_current=True)
    """
    if period_type == "years":
        periods = get_last_years(n)
        if include_current:
            current_period = get_current_year()
            periods.append(current_period)
    elif period_type == "quarters":
        periods = get_last_quarters(n)
        if include_current:
            current_period = get_current_quarter()
            periods.append(current_period)
    elif period_type == "months":
        periods = get_last_months(n)
        if include_current:
            current_period = get_current_month()
            periods.append(current_period)
    elif period_type == "weeks":
        periods = get_last_weeks(n)
        if include_current:
            current_period = get_current_week()
            periods.append(current_period)
    else:
        raise ValueError(
            "Unsupported period type. Use 'years', 'quarters', 'months', or 'weeks'."
        )

    return periods
