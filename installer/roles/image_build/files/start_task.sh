#!/bin/ash

# Wait for database to start accepting connections
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 1
done

# Wait for message broker to start acception connections
while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
  sleep 1
done

case $TEST_MODE in
    "unit")
        echo unit tests; exit $?
    ;;
    "integration")
        echo integration tests; exit $?
    ;;
esac

# Apply any pending migrations
./manage.py makemigrations
./manage.py migrate --no-input

# Preload database and recommendations
if [ -n "$PRELOAD_DATA" ]; then
  ./manage.py loadcsv -users_csv /data/users.csv \
    -books_csv /data/items.csv -ratings_csv /data/ratings.csv
  ./manage.py init_recs
  echo INITED
fi

supervisord -c /supervisor_task.conf
