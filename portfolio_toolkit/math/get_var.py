from typing import Union

import numpy as np
import pandas as pd


def get_covariance_matrix(returns_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the covariance matrix from a DataFrame of logarithmic returns.

    This matrix is used for Value at Risk (VaR) calculations and portfolio optimization.

    Args:
        returns_df (pd.DataFrame): DataFrame where:
            - Rows are dates (datetime index)
            - Columns are ticker symbols
            - Values are logarithmic returns for each asset

    Returns:
        pd.DataFrame: Symmetric covariance matrix where:
            - Rows and columns are ticker symbols
            - Diagonal elements are variances
            - Off-diagonal elements are covariances

    Example:
        >>> dates = pd.date_range('2023-01-01', periods=100, freq='D')
        >>> returns_df = pd.DataFrame({
        ...     'AAPL': np.random.normal(0.001, 0.02, 100),
        ...     'MSFT': np.random.normal(0.0008, 0.018, 100),
        ...     'GOOGL': np.random.normal(0.0012, 0.025, 100)
        ... }, index=dates)
        >>> cov_matrix = get_covariance_matrix(returns_df)
        >>> print(cov_matrix)

    Notes:
        - Uses pandas .cov() method which calculates sample covariance
        - Automatically handles missing values (NaN) by pairwise deletion
        - Matrix is symmetric: cov(A,B) = cov(B,A)
        - Diagonal values are variances: cov(A,A) = var(A)
    """
    if returns_df.empty:
        raise ValueError("Returns DataFrame is empty")

    if len(returns_df) < 2:
        raise ValueError("Need at least 2 observations to calculate covariance")

    # Calculate covariance matrix using pandas built-in method
    covariance_matrix = returns_df.cov()

    return covariance_matrix


def get_correlation_matrix(returns_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the correlation matrix from a DataFrame of logarithmic returns.

    Args:
        returns_df (pd.DataFrame): DataFrame of returns (same format as get_covariance_matrix)

    Returns:
        pd.DataFrame: Correlation matrix with values between -1 and 1

    Example:
        >>> corr_matrix = get_correlation_matrix(returns_df)
    """
    if returns_df.empty:
        raise ValueError("Returns DataFrame is empty")

    return returns_df.corr()


def get_portfolio_variance(
    weights: Union[np.ndarray, pd.Series], covariance_matrix: pd.DataFrame
) -> float:
    """
    Calculates portfolio variance using weights and covariance matrix.

    Formula: σ²_p = w^T * Σ * w
    Where:
        - w = vector of portfolio weights
        - Σ = covariance matrix
        - σ²_p = portfolio variance

    Args:
        weights: Portfolio weights (must sum to 1)
        covariance_matrix: Covariance matrix from get_covariance_matrix()

    Returns:
        float: Portfolio variance

    Example:
        >>> weights = np.array([0.4, 0.4, 0.2])  # 40% AAPL, 40% MSFT, 20% GOOGL
        >>> portfolio_var = get_portfolio_variance(weights, cov_matrix)
    """

    print("Calculating portfolio variance...")
    print(f"Weights: {weights}")

    if isinstance(weights, pd.Series):
        weights = weights.values

    weights = np.array(weights)

    if not np.isclose(weights.sum(), 1.0, rtol=1e-3):
        raise ValueError(f"Weights must sum to 1, got {weights.sum():.4f}")

    if len(weights) != len(covariance_matrix):
        raise ValueError(
            f"Weights length ({len(weights)}) must match covariance matrix size ({len(covariance_matrix)})"
        )

    # Portfolio variance: w^T * Σ * w
    portfolio_variance = np.dot(weights, np.dot(covariance_matrix.values, weights))

    return portfolio_variance


def get_portfolio_volatility(
    weights: Union[np.ndarray, pd.Series], covariance_matrix: pd.DataFrame
) -> float:
    """
    Calculates portfolio volatility (standard deviation).

    Args:
        weights: Portfolio weights
        covariance_matrix: Covariance matrix

    Returns:
        float: Portfolio volatility (sqrt of variance)
    """
    return np.sqrt(get_portfolio_variance(weights, covariance_matrix))


def calculate_var(
    weights: Union[np.ndarray, pd.Series],
    covariance_matrix: pd.DataFrame,
    portfolio_value: float = 1000000,
    confidence_level: float = 0.95,
    time_horizon: int = 1,
) -> float:
    """
    Calculates Value at Risk (VaR) for a portfolio using parametric method.

    VaR represents the maximum expected loss over a given time horizon
    at a specified confidence level, assuming normal distribution of returns.

    Formula: VaR = -z_α * σ_p * √t * V
    Where:
        - z_α = z-score for confidence level (e.g., -1.645 for 95%)
        - σ_p = portfolio volatility (daily)
        - t = time horizon in days
        - V = portfolio value

    Args:
        weights: Portfolio weights (must sum to 1)
        covariance_matrix: Covariance matrix of asset returns
        portfolio_value: Total portfolio value in monetary units (default: 1,000,000)
        confidence_level: Confidence level as decimal (default: 0.95 = 95%)
        time_horizon: Time horizon in days (default: 1 day)

    Returns:
        float: Value at Risk in monetary units (positive value represents potential loss)

    Example:
        >>> weights = np.array([0.4, 0.4, 0.2])
        >>> cov_matrix = get_covariance_matrix(returns_df)
        >>> var_95 = calculate_var(weights, cov_matrix, portfolio_value=1000000)
        >>> print(f"1-day VaR at 95% confidence: ${var_95:,.2f}")

        >>> # 10-day VaR at 99% confidence
        >>> var_99_10d = calculate_var(weights, cov_matrix,
        ...                          portfolio_value=1000000,
        ...                          confidence_level=0.99,
        ...                          time_horizon=10)

    Notes:
        - Assumes normal distribution of returns (parametric VaR)
        - Uses daily volatility from covariance matrix
        - Higher confidence levels give higher VaR values
        - Longer time horizons give higher VaR values (scales with √time)
        - Returns positive value representing potential loss
    """
    from scipy import stats

    if not 0 < confidence_level < 1:
        raise ValueError(
            f"Confidence level must be between 0 and 1, got {confidence_level}"
        )

    if time_horizon <= 0:
        raise ValueError(f"Time horizon must be positive, got {time_horizon}")

    if portfolio_value <= 0:
        raise ValueError(f"Portfolio value must be positive, got {portfolio_value}")

    # Calculate portfolio volatility (daily)
    portfolio_volatility = get_portfolio_volatility(weights, covariance_matrix)

    # Get z-score for confidence level (negative because we want left tail)
    # For 95% confidence, we want 5th percentile = -1.645
    alpha = 1 - confidence_level
    z_score = stats.norm.ppf(alpha)

    # Scale volatility for time horizon (sqrt of time rule)
    scaled_volatility = portfolio_volatility * np.sqrt(time_horizon)

    # Calculate VaR (multiply by -1 to get positive loss value)
    var = -z_score * scaled_volatility * portfolio_value

    return var


def calculate_expected_shortfall(
    weights: Union[np.ndarray, pd.Series],
    covariance_matrix: pd.DataFrame,
    portfolio_value: float = 1000000,
    confidence_level: float = 0.95,
    time_horizon: int = 1,
) -> float:
    """
    Calculates Expected Shortfall (ES) / Conditional Value at Risk (CVaR).

    ES represents the expected loss given that the loss exceeds the VaR threshold.
    It provides information about tail risk beyond VaR.

    Args:
        weights: Portfolio weights
        covariance_matrix: Covariance matrix of asset returns
        portfolio_value: Portfolio value in monetary units
        confidence_level: Confidence level (default: 0.95)
        time_horizon: Time horizon in days (default: 1)

    Returns:
        float: Expected Shortfall in monetary units

    Example:
        >>> es_95 = calculate_expected_shortfall(weights, cov_matrix)
        >>> print(f"Expected Shortfall at 95%: ${es_95:,.2f}")
    """
    from scipy import stats

    if not 0 < confidence_level < 1:
        raise ValueError(
            f"Confidence level must be between 0 and 1, got {confidence_level}"
        )

    # Calculate portfolio volatility
    portfolio_volatility = get_portfolio_volatility(weights, covariance_matrix)

    # Scale for time horizon
    scaled_volatility = portfolio_volatility * np.sqrt(time_horizon)

    # Calculate alpha and z-score
    alpha = 1 - confidence_level
    z_score = stats.norm.ppf(alpha)

    # Expected Shortfall formula for normal distribution
    # ES = μ - σ * φ(z_α) / α
    # Where φ is the standard normal PDF
    phi_z = stats.norm.pdf(z_score)
    expected_shortfall = (
        -(-z_score * scaled_volatility + scaled_volatility * phi_z / alpha)
        * portfolio_value
    )

    return expected_shortfall
