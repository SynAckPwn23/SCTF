#!/bin/bash
# Clean Environment
find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./venv/*" -delete

find . -path "*/migrations/*.pyc" -not -path "./venv/*" -delete
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
