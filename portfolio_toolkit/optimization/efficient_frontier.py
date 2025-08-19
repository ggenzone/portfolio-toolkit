"""
Efficient Frontier Calculation Module

This module provides functions to calculate the efficient frontier for portfolio optimization
using mean-variance optimization theory.
"""

from typing import Dict, List, Union

import numpy as np
import pandas as pd
from scipy.optimize import minimize


def compute_efficient_frontier(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    num_points: int = 100,
    risk_free_rate: float = 0.0,
) -> Dict[str, List[float]]:
    """
    Calculate the efficient frontier for a given set of assets.

    The efficient frontier represents the set of optimal portfolios that offer
    the highest expected return for each level of risk (volatility).

    Parameters:
    -----------
    expected_returns : pd.Series
        Expected returns for each asset. Index should match covariance_matrix columns.
    covariance_matrix : pd.DataFrame
        Covariance matrix of asset returns. Must be symmetric and positive semi-definite.
    num_points : int, default=100
        Number of points to calculate along the efficient frontier.
    risk_free_rate : float, default=0.0
        Risk-free rate for Sharpe ratio calculations.

    Returns:
    --------
    Dict[str, List[float]]
        Dictionary containing:
        - 'volatility': List of portfolio volatilities (standard deviations)
        - 'returns': List of portfolio expected returns
        - 'weights': List of weight arrays for each portfolio

    Example:
    --------
    >>> expected_returns = pd.Series([0.10, 0.12, 0.08], index=['A', 'B', 'C'])
    >>> cov_matrix = pd.DataFrame([[0.05, 0.02, 0.01],
    ...                           [0.02, 0.08, 0.03],
    ...                           [0.01, 0.03, 0.04]],
    ...                          index=['A', 'B', 'C'], columns=['A', 'B', 'C'])
    >>> frontier = get_efficient_frontier(expected_returns, cov_matrix, 50)
    >>> print(f"Min volatility: {min(frontier['volatility']):.4f}")
    >>> print(f"Max return: {max(frontier['returns']):.4f}")
    """

    # Validate inputs
    if not isinstance(expected_returns, pd.Series):
        raise TypeError("expected_returns must be a pandas Series")

    if not isinstance(covariance_matrix, pd.DataFrame):
        raise TypeError("covariance_matrix must be a pandas DataFrame")

    if len(expected_returns) != len(covariance_matrix):
        raise ValueError(
            "Number of assets in expected_returns must match covariance_matrix dimensions"
        )

    if not all(expected_returns.index == covariance_matrix.index):
        raise ValueError("expected_returns index must match covariance_matrix index")

    if not all(expected_returns.index == covariance_matrix.columns):
        raise ValueError(
            "covariance_matrix must be square with matching index and columns"
        )

    if num_points < 2:
        raise ValueError("num_points must be at least 2")

    # Convert to numpy arrays for optimization
    mu = expected_returns.values
    sigma = covariance_matrix.values
    n_assets = len(mu)

    # Calculate minimum variance portfolio
    min_var_weights = _calculate_minimum_variance_portfolio(sigma)
    min_var_return = np.dot(min_var_weights, mu)
    min_var_volatility = np.sqrt(
        np.dot(min_var_weights, np.dot(sigma, min_var_weights))
    )

    # Calculate maximum return portfolio (highest expected return asset with 100% allocation)
    max_return_idx = np.argmax(mu)
    max_return = mu[max_return_idx]

    # Create target returns from min variance return to max return
    target_returns = np.linspace(min_var_return, max_return, num_points)

    # Calculate efficient portfolios for each target return
    efficient_portfolios = []
    efficient_returns = []
    efficient_volatilities = []

    for target_return in target_returns:
        # Optimize portfolio for target return
        weights = _optimize_portfolio_for_target_return(mu, sigma, target_return)

        if weights is not None:
            portfolio_return = np.dot(weights, mu)
            portfolio_volatility = np.sqrt(np.dot(weights, np.dot(sigma, weights)))

            efficient_portfolios.append(weights.tolist())
            efficient_returns.append(portfolio_return)
            efficient_volatilities.append(portfolio_volatility)

    return {
        "volatility": efficient_volatilities,
        "returns": efficient_returns,
        "weights": efficient_portfolios,
    }


def _calculate_minimum_variance_portfolio(covariance_matrix: np.ndarray) -> np.ndarray:
    """
    Calculate the minimum variance portfolio weights.

    Parameters:
    -----------
    covariance_matrix : np.ndarray
        Covariance matrix of asset returns

    Returns:
    --------
    np.ndarray
        Optimal weights for minimum variance portfolio
    """
    n_assets = len(covariance_matrix)

    # Objective function: minimize portfolio variance
    def objective(weights):
        return np.dot(weights, np.dot(covariance_matrix, weights))

    # Constraints: weights sum to 1
    constraints = [{"type": "eq", "fun": lambda x: np.sum(x) - 1.0}]

    # Bounds: weights between 0 and 1 (no short selling)
    bounds = tuple((0, 1) for _ in range(n_assets))

    # Initial guess: equal weights
    x0 = np.array([1.0 / n_assets] * n_assets)

    # Optimize
    result = minimize(
        objective, x0, method="SLSQP", bounds=bounds, constraints=constraints
    )

    if result.success:
        return result.x
    else:
        # Fallback to equal weights if optimization fails
        return x0


def _optimize_portfolio_for_target_return(
    expected_returns: np.ndarray, covariance_matrix: np.ndarray, target_return: float
) -> Union[np.ndarray, None]:
    """
    Optimize portfolio for a specific target return.

    Parameters:
    -----------
    expected_returns : np.ndarray
        Expected returns for each asset
    covariance_matrix : np.ndarray
        Covariance matrix of asset returns
    target_return : float
        Target portfolio return

    Returns:
    --------
    np.ndarray or None
        Optimal weights, or None if optimization fails
    """
    n_assets = len(expected_returns)

    # Objective function: minimize portfolio variance
    def objective(weights):
        return np.dot(weights, np.dot(covariance_matrix, weights))

    # Constraints
    constraints = [
        {"type": "eq", "fun": lambda x: np.sum(x) - 1.0},  # weights sum to 1
        {
            "type": "eq",
            "fun": lambda x: np.dot(x, expected_returns) - target_return,
        },  # target return
    ]

    # Bounds: weights between 0 and 1 (no short selling)
    bounds = tuple((0, 1) for _ in range(n_assets))

    # Initial guess: equal weights
    x0 = np.array([1.0 / n_assets] * n_assets)

    # Optimize
    result = minimize(
        objective, x0, method="SLSQP", bounds=bounds, constraints=constraints
    )

    if result.success:
        return result.x
    else:
        return None


def calculate_portfolio_metrics(
    weights: Union[List[float], np.ndarray],
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    risk_free_rate: float = 0.0,
) -> Dict[str, float]:
    """
    Calculate key portfolio metrics for given weights.

    Parameters:
    -----------
    weights : List[float] or np.ndarray
        Portfolio weights
    expected_returns : pd.Series
        Expected returns for each asset
    covariance_matrix : pd.DataFrame
        Covariance matrix of asset returns
    risk_free_rate : float, default=0.0
        Risk-free rate for Sharpe ratio calculation

    Returns:
    --------
    Dict[str, float]
        Dictionary containing portfolio metrics:
        - 'return': Expected portfolio return
        - 'volatility': Portfolio volatility (standard deviation)
        - 'sharpe_ratio': Sharpe ratio
    """
    weights = np.array(weights)
    mu = expected_returns.values
    sigma = covariance_matrix.values

    portfolio_return = np.dot(weights, mu)
    portfolio_variance = np.dot(weights, np.dot(sigma, weights))
    portfolio_volatility = np.sqrt(portfolio_variance)

    sharpe_ratio = (
        (portfolio_return - risk_free_rate) / portfolio_volatility
        if portfolio_volatility > 0
        else 0
    )

    return {
        "return": portfolio_return,
        "volatility": portfolio_volatility,
        "sharpe_ratio": sharpe_ratio,
    }


def find_maximum_sharpe_portfolio(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    risk_free_rate: float = 0.0,
) -> Dict[str, Union[np.ndarray, float]]:
    """
    Find the portfolio with maximum Sharpe ratio (tangency portfolio).

    Parameters:
    -----------
    expected_returns : pd.Series
        Expected returns for each asset
    covariance_matrix : pd.DataFrame
        Covariance matrix of asset returns
    risk_free_rate : float, default=0.0
        Risk-free rate

    Returns:
    --------
    Dict[str, Union[np.ndarray, float]]
        Dictionary containing:
        - 'weights': Optimal weights
        - 'return': Expected portfolio return
        - 'volatility': Portfolio volatility
        - 'sharpe_ratio': Sharpe ratio
    """
    mu = expected_returns.values
    sigma = covariance_matrix.values
    n_assets = len(mu)

    # Objective function: maximize Sharpe ratio (minimize negative Sharpe ratio)
    def objective(weights):
        portfolio_return = np.dot(weights, mu)
        portfolio_variance = np.dot(weights, np.dot(sigma, weights))
        portfolio_volatility = np.sqrt(portfolio_variance)

        if portfolio_volatility == 0:
            return -np.inf

        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
        return -sharpe_ratio  # Minimize negative Sharpe ratio

    # Constraints: weights sum to 1
    constraints = [{"type": "eq", "fun": lambda x: np.sum(x) - 1.0}]

    # Bounds: weights between 0 and 1 (no short selling)
    bounds = tuple((0, 1) for _ in range(n_assets))

    # Initial guess: equal weights
    x0 = np.array([1.0 / n_assets] * n_assets)

    # Optimize
    result = minimize(
        objective, x0, method="SLSQP", bounds=bounds, constraints=constraints
    )

    if result.success:
        optimal_weights = result.x
        metrics = calculate_portfolio_metrics(
            optimal_weights, expected_returns, covariance_matrix, risk_free_rate
        )

        return {
            "weights": optimal_weights,
            "return": metrics["return"],
            "volatility": metrics["volatility"],
            "sharpe_ratio": metrics["sharpe_ratio"],
        }
    else:
        # Fallback to equal weights
        equal_weights = np.array([1.0 / n_assets] * n_assets)
        metrics = calculate_portfolio_metrics(
            equal_weights, expected_returns, covariance_matrix, risk_free_rate
        )

        return {
            "weights": equal_weights,
            "return": metrics["return"],
            "volatility": metrics["volatility"],
            "sharpe_ratio": metrics["sharpe_ratio"],
        }
