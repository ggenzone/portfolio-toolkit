from dataclasses import dataclass
from datetime import date


@dataclass
class Period:
    """
    Represents a time period with a label and start/end dates.

    Attributes:
        label (str): Human-readable name for the period (e.g., "Q3 2025", "July 2025")
        start_date (date): Start date of the period
        end_date (date): End date of the period

    Example:
        quarter = Period("Q3 2025", date(2025, 7, 1), date(2025, 9, 30))
        month = Period("July 2025", date(2025, 7, 1), date(2025, 7, 31))
    """

    label: str
    start_date: date
    end_date: date

    def __post_init__(self):
        """Validate that end_date is not before start_date."""
        if self.end_date < self.start_date:
            raise ValueError(
                f"End date ({self.end_date}) cannot be before start date ({self.start_date})"
            )

    def __str__(self) -> str:
        """String representation of the period."""
        return f"{self.label} ({self.start_date} to {self.end_date})"
