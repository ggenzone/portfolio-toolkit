from datetime import date
from typing import List

from .period import Period


def get_last_quarters(n=4) -> List[Period]:
    """
    Returns the last n completed quarters as Period objects (excluding current quarter).

    Financial quarters: Q1 (Jan-Mar), Q2 (Apr-Jun), Q3 (Jul-Sep), Q4 (Oct-Dec)

    For n=4 in Q3 2025, returns:
    [Period("Q3 2024", date(2024, 7, 1), date(2024, 9, 30)),
     Period("Q4 2024", date(2024, 10, 1), date(2024, 12, 31)),
     Period("Q1 2025", date(2025, 1, 1), date(2025, 3, 31)),
     Period("Q2 2025", date(2025, 4, 1), date(2025, 6, 30))]

    Args:
        n (int): Number of completed quarters to return

    Returns:
        List[Period]: List of Period objects representing each completed quarter
    """
    today = date.today()
    results = []

    # Determine current quarter and year
    current_quarter = (today.month - 1) // 3 + 1
    current_year = today.year

    for i in range(1, n + 1):  # Start from 1 to exclude current quarter
        # Calculate target quarter and year (go back i quarters)
        target_quarter = current_quarter - i
        target_year = current_year

        # Adjust year if quarter goes negative
        while target_quarter <= 0:
            target_quarter += 4
            target_year -= 1

        # Map quarter to start and end dates
        quarter_dates = {
            1: ((1, 1), (3, 31)),  # Q1: Jan 1 - Mar 31
            2: ((4, 1), (6, 30)),  # Q2: Apr 1 - Jun 30
            3: ((7, 1), (9, 30)),  # Q3: Jul 1 - Sep 30
            4: ((10, 1), (12, 31)),  # Q4: Oct 1 - Dec 31
        }

        # Get start and end dates
        start_month, start_day = quarter_dates[target_quarter][0]
        end_month, end_day = quarter_dates[target_quarter][1]

        start_date = date(target_year, start_month, start_day)
        end_date = date(target_year, end_month, end_day)

        # Create quarter label
        quarter_label = f"Q{target_quarter} {target_year}"

        # Create Period object
        quarter_period = Period(quarter_label, start_date, end_date)
        results.append(quarter_period)

    results.reverse()  # Sort chronologically from oldest to newest

    return results
