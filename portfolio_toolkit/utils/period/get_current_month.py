from datetime import date, datetime, timedelta

from .period import Period


def get_current_month() -> Period:
    """
    Returns information about the current month as a Period object.

    Returns:
        Period: Period object representing the current month

    Example:
        For July 27, 2025:
        Period("July 2025", date(2025, 7, 1), date(2025, 7, 31))
    """
    today = date.today()
    current_year = today.year
    current_month = today.month

    # Start date is first day of current month
    start_date = date(current_year, current_month, 1)

    # End date is last day of current month
    if current_month == 12:
        next_month = 1
        next_year = current_year + 1
    else:
        next_month = current_month + 1
        next_year = current_year

    # Calculate last day by going to first day of next month and subtracting 1 day
    first_day_next_month = datetime(next_year, next_month, 1)
    end_date = (first_day_next_month - timedelta(days=1)).date()

    # Create month label
    month_name = today.strftime("%B")  # Full month name
    month_label = f"{month_name} {current_year}"

    return Period(month_label, start_date, end_date)
