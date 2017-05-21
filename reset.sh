#!/bin/bash
# Clean Environment
find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./venv/*" -delete

find . -path "*/migrations/*.pyc" -not -path "./venv/*" -delete
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate

python manage.py loaddata locations.json


# Test Data
python manage.py loadtestdata accounts.Team:30 -u accounts.fixtures.autofixtures.TeamAutoFixture
python manage.py loadtestdata auth.User:50 -u accounts.fixtures.autofixtures.UserAutoFixture
python manage.py loadtestdata accounts.UserProfile:50

# Admin
echo "
from django.contrib.auth.models import User;
from accounts.models import UserProfile, Team;
from cities_light.models import Country;
admin=User.objects.create_superuser('admin', 'admin@admin.com', 'admin');
team=Team.objects.create(name='admin')

UserProfile.objects.create(
    user=admin,
    job='job',
    gender='M',
    country=Country.objects.get(name='Italy'),
    team=team
);
" | python manage.py shell
