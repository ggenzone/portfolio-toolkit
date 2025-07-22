from dataclasses import dataclass, field
from typing import Any, List, Optional

from .plot_base import PlotBase


@dataclass
class LineChartData(PlotBase):
    """Data structure for line charts"""

    x_data: List[Any] = field(default_factory=list)  # X-axis data
    y_data: List[List[float]] = field(default_factory=list)  # Multiple series
    labels: List[str] = field(default_factory=list)  # Labels for each series
    xlabel: str = "X Axis"
    ylabel: str = "Y Axis"
    colors: Optional[List[str]] = None
    linestyles: Optional[List[str]] = None
    markers: Optional[List[str]] = None

    def get_plot_type(self) -> str:
        return "line"

    def validate(self) -> bool:
        """Validate that data is consistent"""
        if len(self.y_data) != len(self.labels):
            raise ValueError("Y data series and labels must have the same length")

        for i, series in enumerate(self.y_data):
            if len(series) != len(self.x_data):
                raise ValueError(
                    f"Y data series {i} length doesn't match X data length"
                )

        return True
