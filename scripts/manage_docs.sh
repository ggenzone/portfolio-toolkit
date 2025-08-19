#!/bin/bash

# Documentation management script for Portfolio Tools

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Function to check if required tools are installed
check_requirements() {
    print_status "Checking requirements..."
    
    if ! command -v sphinx-build &> /dev/null; then
        print_error "Sphinx not found. Installing..."
        pip install sphinx sphinx-rtd-theme
    fi
    
    if ! command -v python &> /dev/null; then
        print_error "Python not found. Please install Python."
        exit 1
    fi
    
    print_status "Requirements check passed."
}

# Function to clean build directory
clean_docs() {
    local lang=${1:-"all"}
    
    if [ "$lang" = "all" ]; then
        print_status "Cleaning all documentation build directories..."
        rm -rf docs/en/_build docs/es/_build
    else
        print_status "Cleaning documentation build directory for $lang..."
        rm -rf docs/$lang/_build
    fi
    print_status "Documentation cleaned."
}

# Function to build documentation
build_docs() {
    local lang=${1:-"en"}
    
    print_status "Building documentation for language: $lang..."
    cd docs/$lang
    
    # Generate API documentation (only for English to avoid duplication)
    if [ "$lang" = "en" ]; then
        print_status "Generating API documentation..."
        sphinx-apidoc -o api ../../portfolio_toolkit --separate --force
    fi
    
    # Build HTML documentation
    print_status "Building HTML documentation..."
    sphinx-build -b html . _build/html
    
    cd ../..
    print_status "Documentation built successfully for $lang!"
    print_status "Output directory: docs/$lang/_build/html"
}

# Function to serve documentation locally
serve_docs() {
    local lang=${1:-"en"}
    
    print_status "Starting local documentation server for $lang..."
    print_status "Documentation will be available at: http://localhost:8000"
    print_warning "Press Ctrl+C to stop the server"
    
    cd docs/$lang/_build/html
    python -m http.server 8000
}

# Function to deploy to GitHub Pages (requires git setup)
deploy_docs() {
    print_status "Preparing documentation for deployment..."
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository. Cannot deploy."
        exit 1
    fi
    
    # Check if there are uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        print_warning "You have uncommitted changes. Consider committing them first."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Deployment cancelled."
            exit 0
        fi
    fi
    
    # Build documentation first
    build_docs
    
    print_status "Committing documentation changes..."
    git add docs/
    git add .github/workflows/docs.yml
    
    if git diff-index --quiet --cached HEAD --; then
        print_status "No documentation changes to commit."
    else
        git commit -m "Update documentation"
        print_status "Documentation changes committed."
    fi
    
    print_status "Pushing to remote repository..."
    git push origin $(git branch --show-current)
    
    print_status "Documentation deployment initiated!"
    print_status "GitHub Actions will build and deploy the documentation automatically."
    print_status "Check the Actions tab in your GitHub repository for progress."
}

# Function to watch for changes and rebuild automatically
watch_docs() {
    print_status "Setting up documentation auto-rebuild..."
    
    if ! command -v sphinx-autobuild &> /dev/null; then
        print_status "Installing sphinx-autobuild..."
        pip install sphinx-autobuild
    fi
    
    print_status "Starting documentation auto-rebuild server..."
    print_status "Documentation will be available at: http://localhost:8000"
    print_status "Documentation will rebuild automatically when files change."
    print_warning "Press Ctrl+C to stop the server"
    
    cd docs
    sphinx-autobuild . _build/html --host 0.0.0.0 --port 8000
}

# Function to show help
show_help() {
    echo "Portfolio Tools Documentation Manager"
    echo
    echo "Usage: $0 [COMMAND] [LANGUAGE]"
    echo
    echo "Commands:"
    echo "  check              Check if required tools are installed"
    echo "  clean [LANG]       Clean the documentation build directory"
    echo "  build [LANG]       Build the documentation"
    echo "  serve [LANG]       Build and serve documentation locally"
    echo "  watch [LANG]       Auto-rebuild documentation on file changes"
    echo "  deploy             Build and deploy documentation to GitHub Pages"
    echo "  help               Show this help message"
    echo
    echo "Languages:"
    echo "  en                 English (default)"
    echo "  es                 Spanish"
    echo "  all                All languages (for clean command)"
    echo
    echo "Examples:"
    echo "  $0 build en              # Build English documentation"
    echo "  $0 build es              # Build Spanish documentation"
    echo "  $0 serve en              # Build and serve English locally"
    echo "  $0 serve es              # Build and serve Spanish locally"
    echo "  $0 clean all             # Clean all build directories"
}

# Main script logic
case "${1:-}" in
    check)
        check_requirements
        ;;
    clean)
        clean_docs "${2:-all}"
        ;;
    build)
        check_requirements
        build_docs "${2:-en}"
        ;;
    serve)
        check_requirements
        build_docs "${2:-en}"
        serve_docs "${2:-en}"
        ;;
    watch)
        check_requirements
        watch_docs "${2:-en}"
        ;;
    deploy)
        check_requirements
        deploy_docs
        ;;
    help|--help|-h)
        show_help
        ;;
    "")
        print_status "Building and serving English documentation..."
        check_requirements
        build_docs
        serve_docs
        ;;
    *)
        print_error "Unknown command: $1"
        echo
        show_help
        exit 1
        ;;
esac
