from dataclasses import dataclass, field
from typing import List, Optional

from .plot_base import PlotBase


@dataclass
class BarChartData(PlotBase):
    """Data structure for bar charts"""

    labels: List[str] = field(default_factory=list)
    values: List[float] = field(default_factory=list)
    xlabel: str = "Categories"
    ylabel: str = "Values"
    colors: Optional[List[str]] = None
    horizontal: bool = False

    def get_plot_type(self) -> str:
        return "bar"

    def validate(self) -> bool:
        """Validate that data is consistent"""
        if len(self.labels) != len(self.values):
            raise ValueError("Labels and values must have the same length")

        return True
