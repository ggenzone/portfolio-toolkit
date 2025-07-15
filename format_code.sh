#!/bin/bash

# Auto-format code script
echo "🎨 Auto-formatting code..."

echo "=== APPLYING BLACK ==="
black portfolio_tools/

echo -e "\n=== APPLYING ISORT ==="
isort portfolio_tools/

echo -e "\n=== VERIFICATION ==="
echo "Running checks to verify formatting..."

black --check portfolio_tools/ && isort --check-only portfolio_tools/ && flake8 portfolio_tools/

if [ $? -eq 0 ]; then
    echo -e "\n✅ Code formatting completed successfully!"
else
    echo -e "\n❌ Some formatting issues remain. Please check the output above."
    exit 1
fi
