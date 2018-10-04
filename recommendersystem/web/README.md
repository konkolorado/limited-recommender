# Check if models are correctly defined
python manage.py check

# Package model changes into migration files
python manage.py makemigrations

# See what current migrations exist
python manage.py showmigrations

# See the sql commands that will be applied during a migration
python manage.py sqlmigrate <app> <migration_name>

# Apply migrations to database
python manage.py migrate

# Runs a python shell with the django project specific configs loaded
python manage.py shell

# Opens up a connection to the configured django database
python manage.py dbshell
