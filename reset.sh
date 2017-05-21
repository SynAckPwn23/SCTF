#!/bin/bash
# Clean Environment
find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./venv/*" -delete

find . -path "*/migrations/*.pyc" -not -path "./venv/*" -delete
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
# Admin
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@admin.com', 'admin')" | python manage.py shell
# Test Data
python manage.py loadtestdata auth.User:100 -u accounts.fixtures.autofixtures.UserAutoFixture
python manage.py loadtestdata accounts.Team:29 -u accounts.fixtures.autofixtures.TeamAutoFixture
python manage.py loadtestdata accounts.UserProfile:100
