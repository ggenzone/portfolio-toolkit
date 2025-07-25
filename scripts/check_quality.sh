#!/bin/bash

# Quick lint and format check script
echo "🔍 Running code quality checks..."

echo "=== BLACK CHECK ==="
black --check portfolio_toolkit/
BLACK_EXIT=$?

echo -e "\n=== ISORT CHECK ==="
isort --check-only portfolio_toolkit/
ISORT_EXIT=$?

echo -e "\n=== FLAKE8 CHECK ==="
flake8 portfolio_toolkit/
FLAKE8_EXIT=$?

echo -e "\n=== PYTEST ==="
python -m pytest tests/ -v --tb=short
PYTEST_EXIT=$?

# Summary
echo -e "\n📊 SUMMARY:"
if [ $BLACK_EXIT -eq 0 ]; then
    echo "✅ Black formatting: PASSED"
else
    echo "❌ Black formatting: FAILED"
fi

if [ $ISORT_EXIT -eq 0 ]; then
    echo "✅ Import sorting: PASSED"
else
    echo "❌ Import sorting: FAILED"
fi

if [ $FLAKE8_EXIT -eq 0 ]; then
    echo "✅ Flake8 linting: PASSED"
else
    echo "❌ Flake8 linting: FAILED"
fi

if [ $PYTEST_EXIT -eq 0 ]; then
    echo "✅ Tests: PASSED"
else
    echo "❌ Tests: FAILED"
fi

# Exit with error if any check failed
if [ $BLACK_EXIT -ne 0 ] || [ $ISORT_EXIT -ne 0 ] || [ $FLAKE8_EXIT -ne 0 ] || [ $PYTEST_EXIT -ne 0 ]; then
    exit 1
fi

echo -e "\n🎉 All checks passed!"
