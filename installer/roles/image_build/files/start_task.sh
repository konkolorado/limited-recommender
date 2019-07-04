#!/bin/ash

# Wait for database to start accepting connections
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 1
done

# Apply any pending migrations
./manage.py makemigrations
./manage.py migrate --no-input

# Preload database
./manage.py loadcsv -users_csv $USERS \
  -books_csv $BOOKS -ratings_csv $RATINGS

# Run tests
#TODO remove when finished
./manage.py test --noinput

./manage.py init_recommendations
