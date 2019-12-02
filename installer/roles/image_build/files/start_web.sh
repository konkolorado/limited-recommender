#!/bin/ash

# Wait for database to start accepting connections
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 1
done

# Wait for message broker to start acception connections
while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
  sleep 1
done

if [ "$UNIT_TESTS" = true ] ; then
    ./manage.py test api.tests --noinput; exit $?
fi

# Collect static files
./manage.py collectstatic --no-input --link

supervisord -c /supervisor_web.conf
