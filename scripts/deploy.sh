#!/bin/bash

# Portfolio Toolkit deployment script

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [[ ! -f "setup.py" ]] || [[ ! -d "portfolio_toolkit" ]]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Run tests
print_status "Running tests..."
python -m pytest tests/ -v
if [[ $? -ne 0 ]]; then
    print_error "Tests failed. Aborting deployment."
    exit 1
fi

# Run quality checks (if tools are available)
if command -v black &> /dev/null; then
    print_status "Running Black formatter check..."
    black --check portfolio_toolkit/
fi

if command -v isort &> /dev/null; then
    print_status "Running isort check..."
    isort --check-only portfolio_toolkit/
fi

if command -v flake8 &> /dev/null; then
    print_status "Running flake8 check..."
    flake8 portfolio_toolkit/
fi

# Build package
print_status "Building package..."
python -m build

# Check package
print_status "Checking package..."
twine check dist/*

# Ask for confirmation
print_warning "Ready to upload to PyPI!"
print_status "Package: portfolio-toolkit"
print_status "Version: $(python -c 'from portfolio_toolkit import __version__; print(__version__)')"
echo
read -p "Continue with upload? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_status "Upload cancelled."
    exit 0
fi

# Upload to PyPI
print_status "Uploading to PyPI..."
twine upload dist/*

print_status "🎉 Package uploaded successfully!"
print_status "Install with: pip install portfolio-toolkit"