#!/bin/bash

# Apply any pending migartions
python manage.py migrate --no-input

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn recommender_web.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
