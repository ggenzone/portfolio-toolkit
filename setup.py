from setuptools import setup, find_packages

setup(
    name="portfolio-tools",
    version="0.1.0",
    description="Financial portfolio analysis library and CLI.",
    author="Guido Genzone",
    url="https://github.com/ggenzone/portfolio-tools",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "yfinance>=0.2.0",
        "tabulate"
    ],
    entry_points={
        'console_scripts': [
            'portfolio-tools = cli.cli:main',
        ],
    },
    python_requires='>=3.8',
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
