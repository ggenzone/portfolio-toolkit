import click

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.optimization import Optimization

from ..utils import load_json_file


@click.command()
@click.argument("file", type=click.Path(exists=True))
def frontier(file):
    """Show portfolio risk metrics"""
    data = load_json_file(file)
    data_provider = YFDataProvider()
    portfolio = Optimization.from_dict(data, data_provider=data_provider)

    # Calcular frontera eficiente
    frontier = portfolio.get_efficient_frontier(num_points=50)

    # Para graficar
    import matplotlib.pyplot as plt

    plt.plot(frontier["volatility"], frontier["returns"], "b-", linewidth=2)
    plt.xlabel("Volatilidad (Riesgo)")
    plt.ylabel("Retorno Esperado")
    plt.title("Frontera Eficiente")
    plt.show()


# Datos de ejemplo
# expected_returns = pd.Series({
#    'AAPL': 0.12,   # 12% retorno esperado
#    'MSFT': 0.10,   # 10% retorno esperado
#    'GOOGL': 0.14   # 14% retorno esperado
# })

# covariance_matrix = pd.DataFrame({
#    'AAPL':  [0.0400, 0.0180, 0.0220],
#    'MSFT':  [0.0180, 0.0300, 0.0150],
#    'GOOGL': [0.0220, 0.0150, 0.0500]
# }, index=['AAPL', 'MSFT', 'GOOGL'])
