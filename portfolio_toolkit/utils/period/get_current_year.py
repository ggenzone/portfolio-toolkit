from datetime import date

from .period import Period


def get_current_year() -> Period:
    """
    Returns information about the current year as a Period object.

    Returns:
        Period: Period object representing the current year

    Example:
        For July 27, 2025:
        Period("2025", date(2025, 1, 1), date(2025, 12, 31))
    """
    today = date.today()
    current_year = today.year

    start_date = date(current_year, 1, 1)
    end_date = date(current_year, 12, 31)

    year_label = str(current_year)

    return Period(year_label, start_date, end_date)
