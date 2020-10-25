# Digglet

## Setting up the project

Assuming you have `git` and `python3` installed, run the following from the project's root directory:

```bash
# create a virtualenv called venv and activate it
python3 -m venv venv
source ./venv/bin/activate

# install all dependencies
pip install --requirement requirements.txt

# Create a digglet db in your local postgresql server
psql
psql> CREATE DATABASE digglet;

# run all migrations to bring the db schema up-to-date
python manage.py db upgrade

# initialize the database with the following test users:
# - email `user@example.com` with password `Password1`.
# - email `admin@example.com` with password `Password1`.
python manage.py init_db

# create a local_settings.py file to configure the app (replace the values after copying it)
cp app/local_settings_example.py app/local_settings.py

# run the server
FLASK_ENV=development python manage.py runserver
```

## Commands for development

-   format with black and lint with flake8: `black app migrations tests && flake8 app migrations tests`
-   create a new database migration (after model-related changes): `python manage.py db migrate -m "description_of_the_change"`
-   run unit tests: `pytest --cov app --cov-report=term tests`
-   run the development server locally: `FLASK_ENV=development python manage.py runserver --reload`
