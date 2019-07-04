#!/bin/ash

# Wait for database to start accepting connections
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 1
done

# Collect static files
./manage.py collectstatic --no-input --link

supervisord -c /supervisor_web.conf
