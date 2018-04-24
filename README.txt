# Running tests
To run tests, cd to a directory that contains a "test[s]" directory and
run nose2.  This will automatically discover unittests and run them


# Postgresql
The deploy_postgres script will mount the data source directory into the
container and will persist the container data in the directory specified by
PGDATA to the host's local directory specified by PGLOCAL.

Build the postgres image
- cd postgres
- ./build_postgres.sh

Deploy the postgres container
- cd postgres
- ./deploy_postgres.sh

Running tests
- cd postgres/tests
- python test_something.py
