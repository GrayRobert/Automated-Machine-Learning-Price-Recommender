# Requirements
*  Python 3.6+
*  virtualenv python module

# Load the Python Virtual Environment
source venv/bin/activate

# Run the API
cd to src directory
python manage.py runserver

# Database ORM
Django has some object relational model features so we can persist our models into a database with schemas

## Generate the schemas
python manage.py makemigrations recommender

## Persist the schemas
python manage.py migrate
