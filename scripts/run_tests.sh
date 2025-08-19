#!/bin/bash

# Test runner script for Portfolio Tools

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_section() {
    echo -e "${BLUE}[SECTION]${NC} $1"
}

# Function to run unit tests
run_unit_tests() {
    print_section "Running Unit Tests"
    echo "=================================="
    
    if command -v pytest &> /dev/null; then
        python -m pytest tests/ -v
    else
        print_warning "pytest not found, installing..."
        pip install pytest
        python -m pytest tests/ -v
    fi
}

# Function to run unit tests with coverage
run_tests_with_coverage() {
    print_section "Running Unit Tests with Coverage"
    echo "======================================="
    
    if ! command -v pytest &> /dev/null || ! python -c "import pytest_cov" &> /dev/null; then
        print_warning "pytest or pytest-cov not found, installing..."
        pip install pytest pytest-cov
    fi
    
    python -m pytest tests/ -v --cov=portfolio_tools --cov-report=term-missing --cov-report=html
    
    if [ -d "htmlcov" ]; then
        print_status "Coverage report generated in htmlcov/ directory"
        print_status "Open htmlcov/index.html to view detailed coverage report"
    fi
}

# Function to validate example portfolios
validate_examples() {
    print_section "Validating Example Portfolios"
    echo "=============================="
    
    python tests/examples/validate_portfolios.py

    print_section "Validating Example Watchlists"
    echo "=============================="

    python tests/examples/validate_watchlists.py
}

# Function to test CLI commands
test_cli_commands() {
    print_section "Testing CLI Commands"
    echo "===================="

    print_status "Testing portfolio positions command..."
    python -m portfolio_toolkit.cli.cli portfolio positions tests/examples/portfolio/basic_portfolio.json 2025-01-01

    print_status "CLI commands tested successfully!"
}

# Function to run linting
run_linting() {
    print_section "Running Code Quality Checks"
    echo "============================"
    
    print_status "Checking with flake8..."
    if command -v flake8 &> /dev/null; then
        flake8 portfolio_toolkit --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 portfolio_toolkit --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    else
        print_warning "flake8 not found, installing..."
        pip install flake8
        flake8 portfolio_toolkit --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 portfolio_toolkit --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    fi
}

# Function to show help
show_help() {
    echo "Portfolio Tools Test Runner"
    echo
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  unit               Run unit tests only"
    echo "  coverage           Run unit tests with coverage report"
    echo "  examples           Validate example portfolios"
    echo "  cli                Test CLI commands"
    echo "  lint               Run code quality checks"
    echo "  all                Run all tests and checks"
    echo "  help               Show this help message"
    echo
    echo "Examples:"
    echo "  $0 unit            # Run just unit tests"
    echo "  $0 coverage        # Run tests with coverage"
    echo "  $0 all             # Run everything"
}

# Function to run all tests
run_all_tests() {
    print_section "Running All Tests and Checks"
    echo "============================="
    
    echo
    run_unit_tests
    
    echo
    validate_examples
    
    echo
    test_cli_commands
    
    echo
    run_linting
    
    echo
    print_status "All tests and checks completed successfully! ✅"
}

# Main script logic
case "${1:-}" in
    unit)
        run_unit_tests
        ;;
    coverage)
        run_tests_with_coverage
        ;;
    examples)
        validate_examples
        ;;
    cli)
        test_cli_commands
        ;;
    lint)
        run_linting
        ;;
    all)
        run_all_tests
        ;;
    help|--help|-h)
        show_help
        ;;
    "")
        print_status "Running all tests and checks..."
        run_all_tests
        ;;
    *)
        print_error "Unknown command: $1"
        echo
        show_help
        exit 1
        ;;
esac
