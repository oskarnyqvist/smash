#!/bin/bash
set -e

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build package
python3 -m build

# Upload to TestPyPI
twine upload --repository testpypi dist/*
