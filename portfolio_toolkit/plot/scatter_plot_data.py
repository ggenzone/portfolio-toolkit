from dataclasses import dataclass, field
from typing import List, Optional

from .plot_base import PlotBase


@dataclass
class ScatterPlotData(PlotBase):
    """Data structure for scatter plots"""

    x_data: List[float] = field(default_factory=list)
    y_data: List[float] = field(default_factory=list)
    labels: Optional[List[str]] = None
    xlabel: str = "X Axis"
    ylabel: str = "Y Axis"
    colors: Optional[List[str]] = None
    sizes: Optional[List[float]] = None
    alpha: float = 0.7

    def get_plot_type(self) -> str:
        return "scatter"

    def validate(self) -> bool:
        """Validate that data is consistent"""
        if len(self.x_data) != len(self.y_data):
            raise ValueError("X and Y data must have the same length")

        if self.labels and len(self.labels) != len(self.x_data):
            raise ValueError("Labels must match data length")

        return True
