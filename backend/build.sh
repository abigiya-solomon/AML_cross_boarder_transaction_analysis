#!/usr/bin/env bash
set -o errexit

echo "Installing backend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Generating ML artifacts..."
if [ -f "../ml/generate_artifacts.py" ]; then
    python ../ml/generate_artifacts.py
elif [ -f "generate_artifacts.py" ]; then
    python generate_artifacts.py
fi

echo "Build complete."
