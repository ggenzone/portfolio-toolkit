Instalación
===========

Requisitos del Sistema
----------------------

- Python 3.9 o superior
- pip (gestor de paquetes de Python)

Instalación desde el Repositorio
--------------------------------

Para desarrollo local, clona el repositorio e instala en modo editable:

.. code-block:: bash

    git clone https://github.com/ggenzone/portfolio-toolkit.git
    cd portfolio-toolkit
    pip install -e .

Instalación de Dependencias
---------------------------

Instala las dependencias necesarias:

.. code-block:: bash

    pip install -r requirements.txt

Para documentación:

.. code-block:: bash

    pip install -r docs-requirements.txt

Verificación de la Instalación
------------------------------

Verifica que la instalación fue exitosa:

.. code-block:: python

    import portfolio_toolkit
    print(portfolio_toolkit.__version__)

También puedes probar la interfaz de línea de comandos:

.. code-block:: bash

    portfolio-tools --help
