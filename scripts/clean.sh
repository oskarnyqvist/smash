#!/bin/bash
set -e

echo "🧹 Cleaning Python build and cache artifacts..."

# Delete Python cache files and folders
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete

# Delete build artifacts
rm -rf build/ dist/ *.egg-info

echo "✅ Clean complete."
