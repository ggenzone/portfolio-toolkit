import matplotlib.pyplot as plt
import pandas as pd


def plot_evolution(df_portfolio):
    """
    Generates a chart showing the evolution of the portfolio value over time.

    Args:
        df_portfolio (pd.DataFrame): Structured DataFrame with the portfolio evolution.

    Returns:
        None
    """
    if df_portfolio is None or df_portfolio.empty:
        print("Error: No data available in the DataFrame to generate the plot.")
        return

    df_pivot = df_portfolio.pivot_table(
        index="Date", columns="Ticker", values="Value_Base", aggfunc="sum", fill_value=0
    )
    df_pivot.sort_index(inplace=True)
    dates = pd.to_datetime(df_pivot.index)
    values = df_pivot.sum(axis=1).values

    plt.figure(figsize=(12, 8))
    plt.fill_between(
        dates, values, 0, color="skyblue", alpha=0.5, label="Area under the curve"
    )
    plt.plot(
        dates,
        values,
        marker="o",
        linestyle="-",
        color="blue",
        linewidth=2,
        label="Portfolio Value",
    )
    plt.title("Portfolio Value Evolution", fontsize=16)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Total Value (USD)", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.show()


def plot_evolution_stacked(df_portfolio):
    """
    Generates a stacked area chart showing the evolution of the portfolio value by ticker.

    Args:
        df_portfolio (pd.DataFrame): Structured DataFrame with the portfolio evolution.

    Returns:
        None
    """
    df_pivot = df_portfolio.pivot_table(
        index="Date", columns="Ticker", values="Value_Base", aggfunc="sum", fill_value=0
    )
    df_pivot.sort_index(inplace=True)
    dates = pd.to_datetime(df_pivot.index)
    values = df_pivot.fillna(0).values.T.astype(float)

    plt.figure(figsize=(12, 6))
    plt.stackplot(dates, values, labels=df_pivot.columns, alpha=0.4)
    plt.title("Portfolio Value Evolution by Ticker")
    plt.xlabel("Date")
    plt.ylabel("Total Value (USD)")
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()


def plot_evolution_vs_cost(df_portfolio):
    """
    Plots the evolution of the portfolio value along with the cost of the shares.

    Args:
        df_portfolio (pd.DataFrame): DataFrame with the portfolio evolution.

    Returns:
        None
    """
    if df_portfolio is None or df_portfolio.empty:
        print("Error: No data available to generate the plot.")
        return

    # Group by date and sum values and costs
    df_grouped = (
        df_portfolio.groupby("Date")
        .agg({"Value_Base": "sum", "Cost": "sum"})
        .reset_index()
    )

    # Extract data
    dates = pd.to_datetime(df_grouped["Date"])
    values = df_grouped["Value_Base"]
    costs = df_grouped["Cost"]

    # Create the plot
    plt.figure(figsize=(12, 8))
    plt.plot(dates, values, label="Portfolio Value", color="blue", linewidth=2)
    plt.plot(
        dates,
        costs,
        label="Cost (Invested Capital)",
        color="orange",
        linestyle="--",
        linewidth=2,
    )
    plt.fill_between(
        dates,
        costs,
        values,
        where=(values > costs),
        color="green",
        alpha=0.3,
        label="Potential Gain",
    )
    plt.fill_between(
        dates,
        costs,
        values,
        where=(values <= costs),
        color="red",
        alpha=0.3,
        label="Potential Loss",
    )
    plt.title("Portfolio Value Evolution vs Cost", fontsize=16)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("USD", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.show()


def plot_evolution_ticker(df_portfolio, ticker):
    """
    Plots the evolution of the value of a specific ticker in the portfolio, including the accumulated cost.

    Args:
        df_portfolio (pd.DataFrame): Structured DataFrame with the portfolio evolution.
        ticker (str): The asset symbol.

    Returns:
        None
    """
    if df_portfolio is None or df_portfolio.empty:
        print("Error: No data available to generate the plot.")
        return

    # Filter data for the specific ticker
    df_ticker = df_portfolio[df_portfolio["Ticker"] == ticker]

    if df_ticker.empty:
        print(f"Error: No data available for ticker {ticker}.")
        return

    dates = pd.to_datetime(df_ticker["Date"])
    values = df_ticker["Value_Base"]
    costs = df_ticker["Cost"]

    # Create the plot
    plt.figure(figsize=(12, 8))
    plt.plot(dates, values, label="Ticker Value", color="blue", linewidth=2)
    plt.plot(
        dates, costs, label="Ticker Cost", color="orange", linestyle="--", linewidth=2
    )
    plt.fill_between(
        dates,
        costs,
        values,
        where=(values > costs),
        color="green",
        alpha=0.3,
        label="Potential Gain",
    )
    plt.fill_between(
        dates,
        costs,
        values,
        where=(values <= costs),
        color="red",
        alpha=0.3,
        label="Potential Loss",
    )
    plt.title(f"Evolution of Ticker {ticker}", fontsize=16)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("USD", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.show()
