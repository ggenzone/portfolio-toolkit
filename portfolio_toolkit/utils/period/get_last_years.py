from datetime import date
from typing import List

from .period import Period


def get_last_years(n=4) -> List[Period]:
    """
    Returns the last n years as Period objects.

    For n=4 in year 2025, returns:
    [Period("2022", date(2022, 1, 1), date(2022, 12, 31)),
     Period("2023", date(2023, 1, 1), date(2023, 12, 31)),
     Period("2024", date(2024, 1, 1), date(2024, 12, 31)),
     Period("2025", date(2025, 1, 1), date(2025, 12, 31))]

    Args:
        n (int): Number of years to return

    Returns:
        List[Period]: List of Period objects representing each year
    """
    today = date.today()
    results = []

    for i in range(n):
        # Get the current year minus i years
        target_year = today.year - i

        # Create start and end dates for the year
        start_date = date(target_year, 1, 1)
        end_date = date(target_year, 12, 31)

        # Create year label
        year_label = str(target_year)

        # Create Period object
        year_period = Period(year_label, start_date, end_date)
        results.append(year_period)

    results.reverse()  # Sort chronologically from oldest to newest

    return results
