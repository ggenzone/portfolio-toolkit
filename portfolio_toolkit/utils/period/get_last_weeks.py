from datetime import date, timedelta
from typing import List

from .period import Period


def get_last_weeks(n=4) -> List[Period]:
    """
    Returns the last n completed weeks as Period objects (excluding current week).

    For n=4 in week 30 of 2025, returns:
    [Period("W26 2025", date(2025, 6, 23), date(2025, 6, 29)),
     Period("W27 2025", date(2025, 6, 30), date(2025, 7, 6)),
     Period("W28 2025", date(2025, 7, 7), date(2025, 7, 13)),
     Period("W29 2025", date(2025, 7, 14), date(2025, 7, 20))]

    Args:
        n (int): Number of completed weeks to return

    Returns:
        List[Period]: List of Period objects representing each completed week
    """
    today = date.today()
    results = []

    for i in range(1, n + 1):  # Start from 1 to exclude current week
        # Go back i weeks from today
        target_date = today - timedelta(weeks=i)
        # Get ISO year, week, and day
        iso_year, iso_week, _ = target_date.isocalendar()

        # Get Monday (day 1) and Sunday (day 7) of that ISO week
        monday = date.fromisocalendar(iso_year, iso_week, 1)
        sunday = date.fromisocalendar(iso_year, iso_week, 7)

        # Create week label
        week_label = f"W{iso_week} {iso_year}"

        # Create Period object
        week_period = Period(week_label, monday, sunday)
        results.append(week_period)

    results.reverse()  # Sort chronologically from oldest to newest

    return results
