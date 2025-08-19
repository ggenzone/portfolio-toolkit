[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/ggenzone/portfolio-toolkit/blob/master/README.md)
[![es](https://img.shields.io/badge/lang-es-green.svg)](https://github.com/ggenzone/portfolio-toolkit/blob/master/README.es.md)

## 📚 Documentación

**[📖 Documentación Completa](https://ggenzone.github.io/portfolio-toolkit/)** - Referencia completa de la API, guías de usuario y ejemplos

### Enlaces Rápidos de Documentación

- **[Primeros Pasos](https://ggenzone.github.io/portfolio-toolkit/examples/basic_usage.html)** - Ejemplos de uso básico
- **[Guía de Uso de CLI](https://ggenzone.github.io/portfolio-toolkit/examples/cli_usage.html)** - Referencia completa de la interfaz de línea de comandos
- **[Soporte Multi-Moneda](https://ggenzone.github.io/portfolio-toolkit/examples/multi_currency.html)** - Trabajando con múltiples monedas
- **[Formato JSON de Cartera](https://ggenzone.github.io/portfolio-toolkit/user_guide/portfolio_format.html)** - Especificación completa del formato
- **[Referencia API](https://ggenzone.github.io/portfolio-toolkit/api/modules.html)** - Documentación completa de la API

### Compilar Documentación Localmente

```bash
# Instalar dependencias de documentación
pip install -r docs-requirements.txt

# Compilar documentación en inglés
./scripts/manage_docs.sh build en

# Compilar documentación en español
./scripts/manage_docs.sh build es

# Servir documentación localmente (inglés)
./scripts/manage_docs.sh serve en

# Servir documentación localmente (español)
./scripts/manage_docs.sh serve es

# Auto-recompilar con cambios (inglés)
./scripts/manage_docs.sh watch en
```

# Documentación de la Biblioteca Portfolio-tools

![Documentation](https://img.shields.io/badge/docs-sphinx-brightgreen.svg)
![Tests](https://github.com/ggenzone/portfolio-toolkit/workflows/Tests%20and%20Quality%20Checks/badge.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)

Esta biblioteca proporciona herramientas para análisis financiero, gestión de carteras y visualización de datos de mercado con soporte integral para múltiples monedas y cálculo de costos FIFO.

## 📚 Documentación

**[📖 Documentación Completa](https://ggenzone.github.io/portfolio-toolkit/)** - Referencia completa de la API, guías de usuario y ejemplos

### Enlaces Rápidos de Documentación

- **[Primeros Pasos](https://ggenzone.github.io/portfolio-toolkit/examples/basic_usage.html)** - Ejemplos de uso básico
- **[Guía de Uso de CLI](https://ggenzone.github.io/portfolio-toolkit/examples/cli_usage.html)** - Referencia completa de la interfaz de línea de comandos
- **[Soporte Multi-Moneda](https://ggenzone.github.io/portfolio-toolkit/examples/multi_currency.html)** - Trabajando con múltiples monedas
- **[Formato JSON de Cartera](https://ggenzone.github.io/portfolio-toolkit/user_guide/portfolio_format.html)** - Especificación completa del formato
- **[Referencia API](https://ggenzone.github.io/portfolio-toolkit/api/modules.html)** - Documentación completa de la API

### Compilar Documentación Localmente

```bash
# Instalar dependencias de documentación
pip install sphinx sphinx-rtd-theme

# Compilar documentación
./manage_docs.sh build

# Servir documentación localmente
./manage_docs.sh serve

# Auto-recompilar con cambios
./manage_docs.sh watch
```

## Calidad de Código

Este proyecto mantiene altos estándares de calidad de código usando:

- **Black** - Formateo de código
- **isort** - Ordenamiento de imports  
- **flake8** - Linting
- **pytest** - Testing

### Verificaciones Rápidas de Calidad

```bash
# Ejecutar todas las verificaciones de calidad
./check_quality.sh

# Auto-formatear código
./format_code.sh

# Herramientas individuales
black portfolio_toolkit/      # Formatear código
isort portfolio_toolkit/      # Ordenar imports
flake8 portfolio_toolkit/     # Lint código
pytest tests/              # Ejecutar tests
```

### Configuración

Las herramientas de calidad de código están configuradas en `pyproject.toml` y `setup.cfg`:
- Longitud de línea: 88 caracteres
- Perfiles de Black e isort: compatibles
- flake8 ignora: E203, E501, W503

## Instalación

Instalar desde la raíz del proyecto (desarrollo local):

```bash
pip install .
```
O en modo editable (recomendado para desarrollo):
```bash
pip install -e .
```

Para desinstalar:
```bash
pip uninstall portfolio-toolkit
```

## Testing

### Ejecutar Tests

```bash
# Ejecutar todos los tests y verificaciones
./run_tests.sh

# Ejecutar suites de tests específicos
./run_tests.sh unit         # Solo tests unitarios
./run_tests.sh coverage     # Tests con reporte de cobertura
./run_tests.sh examples     # Validar carteras de ejemplo
./run_tests.sh cli          # Testear comandos CLI
./run_tests.sh lint         # Verificaciones de calidad de código
```

### Testing Manual

```bash
# Ejecutar tests unitarios directamente
python -m pytest tests/ -v

# Validar carteras de ejemplo
python tests/validate_examples.py

# Testear comandos CLI
portfolio-tools print-positions -f tests/examples/basic_portfolio.json

# O usando el módulo directamente
python -m portfolio_toolkit.cli.cli portfolio print performance-summary tests/examples/basic_portfolio.json

```

## Documentación

```bash
# Desarrollo local
./manage_docs.sh build      # Compilar documentación
./manage_docs.sh serve      # Servir localmente
./manage_docs.sh watch      # Auto-recompilar con cambios

# Desplegar
./manage_docs.sh deploy     # Desplegar a GitHub Pages
```

## Por Hacer

- [x] Agregar tests unitarios y de integración para todos los módulos
- [x] Documentar todos los métodos públicos con ejemplos de uso
- [x] Soporte para carteras multi-moneda y conversión automática de monedas
- [ ] Agregar soporte para más proveedores de datos (ej. Alpha Vantage, IEX Cloud)
- [ ] Permitir cargar carteras desde archivos Excel y ODS nativamente
- [ ] Implementar métricas de rendimiento de cartera (Sharpe, Sortino, drawdown, etc.)
- [ ] Agregar visualizaciones interactivas (ej. con Plotly o Dash)
- [ ] Documentar todos los métodos públicos con ejemplos de uso
- [ ] Agregar exportación a reportes PDF/Excel
- [ ] Permitir simulaciones de rebalanceo y optimización de carteras
- [ ] Agregar análisis de riesgo y Valor en Riesgo (VaR)
- [x] Mejorar interfaz CLI para automatización de tareas (migrado al