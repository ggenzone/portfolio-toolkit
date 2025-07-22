from dataclasses import dataclass, field
from typing import List, Optional

from .plot_base import PlotBase


@dataclass
class PieChartData(PlotBase):
    """Data structure for pie charts"""

    labels: List[str] = field(default_factory=list)
    values: List[float] = field(default_factory=list)
    colors: Optional[List[str]] = None
    autopct: str = "%1.1f%%"
    startangle: float = 90
    explode: Optional[List[float]] = None

    def get_plot_type(self) -> str:
        return "pie"

    def validate(self) -> bool:
        """Validate that data is consistent"""
        if len(self.labels) != len(self.values):
            raise ValueError("Labels and values must have the same length")

        if self.colors and len(self.colors) != len(self.labels):
            raise ValueError("Colors list must match labels length")

        if self.explode and len(self.explode) != len(self.labels):
            raise ValueError("Explode list must match labels length")

        return True
