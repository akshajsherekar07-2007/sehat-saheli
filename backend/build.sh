#!/bin/bash
# Render build script — installs deps and runs migrations
set -e

echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "Running database migrations..."
python -m alembic upgrade head

echo "Build complete!"
