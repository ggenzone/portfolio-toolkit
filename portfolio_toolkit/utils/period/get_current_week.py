from datetime import date

from .period import Period


def get_current_week() -> Period:
    """
    Returns information about the current ISO week as a Period object.

    Returns:
        Period: Period object representing the current ISO week

    Example:
        For July 27, 2025 (which is in ISO week 30):
        Period("W30 2025", date(2025, 7, 21), date(2025, 7, 27))
    """
    today = date.today()

    # Get ISO year, week, and day
    iso_year, iso_week, iso_day = today.isocalendar()

    # Get Monday (day 1) and Sunday (day 7) of current ISO week
    monday = date.fromisocalendar(iso_year, iso_week, 1)
    sunday = date.fromisocalendar(iso_year, iso_week, 7)

    # Create week label
    week_label = f"W{iso_week} {iso_year}"

    return Period(week_label, monday, sunday)
