#!/bin/sh

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
daphne -b 0.0.0.0 -p 8000 settings.asgi:application
