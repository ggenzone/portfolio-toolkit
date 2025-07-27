from datetime import date, datetime, timedelta
from typing import List

from .period import Period


def get_last_months(n=4) -> List[Period]:
    """
    Returns the last n completed months as Period objects (excluding current month).

    For n=4 in July 2025, returns:
    [Period("March 2025", date(2025, 3, 1), date(2025, 3, 31)),
     Period("April 2025", date(2025, 4, 1), date(2025, 4, 30)),
     Period("May 2025", date(2025, 5, 1), date(2025, 5, 31)),
     Period("June 2025", date(2025, 6, 1), date(2025, 6, 30))]

    Args:
        n (int): Number of completed months to return

    Returns:
        List[Period]: List of Period objects representing each completed month
    """
    today = date.today()
    results = []

    for i in range(1, n + 1):  # Start from 1 to exclude current month
        # Go back i months from current month
        target_month = today.month - i
        target_year = today.year

        # Adjust year if month goes negative
        while target_month <= 0:
            target_month += 12
            target_year -= 1

        # Start date is first day of target month
        start_date = date(target_year, target_month, 1)

        # End date is last day of target month
        if target_month == 12:
            next_month = 1
            next_year = target_year + 1
        else:
            next_month = target_month + 1
            next_year = target_year

        # Last day = first day of next month minus 1 day
        first_day_next_month = datetime(next_year, next_month, 1)
        end_date = (first_day_next_month - timedelta(days=1)).date()

        # Create month label
        month_name = start_date.strftime("%B")  # Full month name
        month_label = f"{month_name} {target_year}"

        # Create Period object
        month_period = Period(month_label, start_date, end_date)
        results.append(month_period)

    results.reverse()  # Sort chronologically from oldest to newest

    return results
