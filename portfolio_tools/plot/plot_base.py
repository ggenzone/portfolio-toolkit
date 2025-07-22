from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PlotBase(ABC):
    """Base class for all plot data structures"""

    title: str
    grid: bool = True
    figsize: tuple = (10, 6)

    @abstractmethod
    def get_plot_type(self) -> str:
        """Return the type of plot"""
        pass
