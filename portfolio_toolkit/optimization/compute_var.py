from portfolio_toolkit.math.get_var import calculate_expected_shortfall, calculate_var

from .optimization import Optimization


def compute_var(optimization: Optimization) -> float:
    """
    Computes Value at Risk (VaR) for a portfolio based on optimization results.

    Args:
        optimization (Optimization): Optimization object containing portfolio weights and covariance matrix.

    Returns:
        float: Value at Risk in monetary units.
    """
    weights = [asset.quantity for asset in optimization.assets]

    covariance_matrix = optimization.covariance_matrix

    portfolio_value = 10000  # $5M portfolio
    confidence_level = 0.95  # 99% confianza
    time_horizon = 10  # 10 días

    # Calculate VaR for the portfolio
    var_10_95 = calculate_var(
        weights, covariance_matrix, portfolio_value, confidence_level, time_horizon
    )

    # Expected Shortfall
    es_10_95 = calculate_expected_shortfall(
        weights, covariance_matrix, portfolio_value, confidence_level, time_horizon
    )

    print(f"10-day VaR at 95% confidence: ${var_10_95:,.2f}")
    print(f"Expected Shortfall: ${es_10_95:,.2f}")

    return var_10_95
