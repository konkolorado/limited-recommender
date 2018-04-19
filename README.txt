Deploying all tests in docker environment
- ./deploy_tests.sh

Running tests
- Run all tests
- $ python3.6 -m unittest discover

- Run tests specific to a module
- $ python3.6 -m unittest module.test_something


# Postgresql
The deploy_postgres script will mount the data source directory into the
container and will persist the container data in the directory specified by
PGDATA to the host's local directory specified by PGLOCAL 

Build the postgres image
- cd postgres
- ./build_postgres.sh

Deploy the postgres container
- cd postgres
- ./deploy_postgres.sh

Running tests
- cd postgres/tests
- python test_something.py
