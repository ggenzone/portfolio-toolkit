from .get_current_month import get_current_month
from .get_current_quarter import get_current_quarter
from .get_current_week import get_current_week
from .get_current_year import get_current_year
from .period import Period


def get_current_period(period_type: str) -> Period:
    """
    Returns the current period as a Period object based on the specified type.

    Args:
        period_type (str): Type of period ('year', 'quarter', 'month', 'week')

    Returns:
        Period: Period object representing the current period

    Raises:
        ValueError: If period_type is not supported

    Example:
        current_week = get_current_period('week')
        current_quarter = get_current_period('quarter')
        current_year = get_current_period('year')
    """
    if period_type == "year":
        return get_current_year()
    elif period_type == "quarter":
        return get_current_quarter()
    elif period_type == "month":
        return get_current_month()
    elif period_type == "week":
        return get_current_week()
    else:
        raise ValueError(
            f"Unsupported period type '{period_type}'. "
            "Use 'year', 'quarter', 'month', or 'week'."
        )
