#!/bin/bash

echo "VERCEL_ENV: $VERCEL_ENV"

if [[ "$VERCEL_ENV" == "production" ]]; then
    # Proceed with the build
    echo "✅ - Build can proceed"

    # Create a virtual environment
    echo "Creating a virtual environment..."
    python3.12 -m venv venv
    source venv/bin/activate

    # Install the latest version of pip
    echo "Installing the latest version of pip..."
    python -m pip install --upgrade pip

    # Build the project
    echo "Building the project..."
    python -m pip install -r requirements.txt

    # Migrations
    # echo "Database migration..."
    # python manage.py migrate --noinput

    # Collect static files
    echo "Collecting static files..."
    python manage.py collectstatic --noinput --verbosity 2
else
    # Don't build
    echo "🛑 - Build cancelled"
    exit 0
fi