#!/bin/ash

# Wait for database to start accepting connections
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 1
done

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
python manage.py collectstatic --no-input --link

supervisord -c /supervisor.conf
