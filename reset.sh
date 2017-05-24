#!/bin/bash
# Clean Environment
find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./venv/*" -delete

find . -path "*/migrations/*.pyc" -not -path "./venv/*" -delete
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate

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
    country=Country.objects.get_or_create(name='Italy')[0],
    team=team
);
" | python manage.py shell
