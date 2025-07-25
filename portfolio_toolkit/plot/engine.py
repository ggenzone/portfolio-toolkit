from typing import Optional

import matplotlib.pyplot as plt

from .bar_chart_data import BarChartData
from .line_chart_data import LineChartData
from .pie_chart_data import PieChartData
from .plot_base import PlotBase
from .scatter_plot_data import ScatterPlotData


class PlotEngine:
    """Universal plotting engine that can handle different plot types"""

    @staticmethod
    def plot(
        data: PlotBase, save_path: Optional[str] = None, show: bool = True
    ) -> None:
        """
        Plot data based on its type

        Args:
            data: Plot data structure inheriting from PlotBase
            save_path: Optional path to save the plot
            show: Whether to display the plot
        """
        # Validate data before plotting
        data.validate()

        # Create figure with specified size
        plt.figure(figsize=data.figsize)

        # Route to appropriate plotting method
        if isinstance(data, PieChartData):
            PlotEngine._plot_pie(data)
        elif isinstance(data, LineChartData):
            PlotEngine._plot_line(data)
        elif isinstance(data, BarChartData):
            PlotEngine._plot_bar(data)
        elif isinstance(data, ScatterPlotData):
            PlotEngine._plot_scatter(data)
        else:
            raise ValueError(f"Unsupported plot type: {type(data)}")

        # Set title and grid
        plt.title(data.title)
        if data.grid:
            plt.grid(True, alpha=0.3)

        # Save if path provided
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        # Show if requested
        if show:
            plt.show()
        else:
            plt.close()

    @staticmethod
    def _plot_pie(data: PieChartData) -> None:
        """Plot pie chart"""
        plt.pie(
            data.values,
            labels=data.labels,
            colors=data.colors,
            autopct=data.autopct,
            startangle=data.startangle,
            explode=data.explode,
        )
        plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle

    @staticmethod
    def _plot_line(data: LineChartData) -> None:
        """Plot line chart"""
        for i, (y_series, label) in enumerate(zip(data.y_data, data.labels)):
            color = data.colors[i] if data.colors else None
            linestyle = data.linestyles[i] if data.linestyles else "-"
            marker = data.markers[i] if data.markers else None

            plt.plot(
                data.x_data,
                y_series,
                label=label,
                color=color,
                linestyle=linestyle,
                marker=marker,
            )

        plt.xlabel(data.xlabel)
        plt.ylabel(data.ylabel)
        plt.legend()

    @staticmethod
    def _plot_bar(data: BarChartData) -> None:
        """Plot bar chart"""
        if data.horizontal:
            plt.barh(data.labels, data.values, color=data.colors)
            plt.xlabel(data.ylabel)
            plt.ylabel(data.xlabel)
        else:
            plt.bar(data.labels, data.values, color=data.colors)
            plt.xlabel(data.xlabel)
            plt.ylabel(data.ylabel)

        # Rotate x-axis labels if needed
        if not data.horizontal and len(data.labels) > 5:
            plt.xticks(rotation=45, ha="right")

    @staticmethod
    def _plot_scatter(data: ScatterPlotData) -> None:
        """Plot scatter plot"""
        plt.scatter(
            data.x_data, data.y_data, c=data.colors, s=data.sizes, alpha=data.alpha
        )

        plt.xlabel(data.xlabel)
        plt.ylabel(data.ylabel)

        # Add labels if provided
        if data.labels:
            for i, label in enumerate(data.labels):
                plt.annotate(label, (data.x_data[i], data.y_data[i]))
