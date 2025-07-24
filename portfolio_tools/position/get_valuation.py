from typing import List

from portfolio_tools.position.valued_position import ValuedPosition


def get_valuation(open_positions: List[ValuedPosition]) -> float:
    """
    Prints the valuation of open positions.

    Args:
        open_positions (List[ValuedPosition]): List of ValuedPosition objects representing open positions.

    Returns:
        None
    """

    total_value = 0
    for position in open_positions:
        total_value += position.value

    return total_value
