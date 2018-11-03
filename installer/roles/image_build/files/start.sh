#!/bin/ash

# Apply any pending migrations
python manage.py makemigrations
python manage.py migrate --no-input

# Preload database
python manage.py loadcsv -users_csv $USERS \
  -books_csv $BOOKS -ratings_csv $RATINGS

# Run tests
#TODO remove when finished
python manage.py test --noinput

# Collect static files
python manage.py collectstatic --no-input

supervisord -c /supervisor.conf
