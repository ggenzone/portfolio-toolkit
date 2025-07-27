from datetime import date

from .period import Period


def get_current_quarter() -> Period:
    """
    Returns information about the current financial quarter as a Period object.

    Returns:
        Period: Period object representing the current quarter

    Example:
        For July 27, 2025:
        Period("Q3 2025", date(2025, 7, 1), date(2025, 9, 30))
    """
    today = date.today()
    current_quarter = (today.month - 1) // 3 + 1
    current_year = today.year

    # Define quarter boundaries
    quarter_boundaries = {
        1: ((1, 1), (3, 31)),  # Q1: Jan 1 - Mar 31
        2: ((4, 1), (6, 30)),  # Q2: Apr 1 - Jun 30
        3: ((7, 1), (9, 30)),  # Q3: Jul 1 - Sep 30
        4: ((10, 1), (12, 31)),  # Q4: Oct 1 - Dec 31
    }

    # Get start and end dates for current quarter
    start_month, start_day = quarter_boundaries[current_quarter][0]
    end_month, end_day = quarter_boundaries[current_quarter][1]

    start_date = date(current_year, start_month, start_day)
    end_date = date(current_year, end_month, end_day)

    # Create quarter label
    quarter_label = f"Q{current_quarter} {current_year}"

    return Period(quarter_label, start_date, end_date)
