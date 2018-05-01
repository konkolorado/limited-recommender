#!/bin/bash

# Apply any pending migrations
python manage.py makemigrations
python manage.py migrate --no-input

# Preload database
python manage.py loadcsv -users_csv $USERS \
  -books_csv $BOOKS -ratings_csv $RATINGS

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn recommender_web.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
