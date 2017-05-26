#!/bin/bash

# Locations
python manage.py loaddata locations.json


# Challenges Categories
python manage.py loaddata categories.json


# Challenges
python manage.py loadtestdata challenges.Challenge:50 -u challenges.fixtures.autofixtures.ChallengeAutoFixture


# Users Data
python manage.py loadtestdata accounts.Team:10 -u accounts.fixtures.autofixtures.TeamAutoFixture
python manage.py loadtestdata auth.User:50 -u accounts.fixtures.autofixtures.UserAutoFixture
python manage.py loadtestdata accounts.UserProfile:50 -u accounts.fixtures.autofixtures.UserProfileAutoFixture


# Admin
echo "
from django.contrib.auth.models import User;
from accounts.models import UserProfile, Team;
from cities_light.models import Country;
from challenges.models import Challenge, ChallengeSolved;
from django.utils.timezone import now, timedelta
import random

start = now() - timedelta(days=30)
admin=User.objects.create_superuser('admin', 'admin@admin.com', 'admin');
admin.created_at = start
admin.save()

team=Team.objects.create(name='admin')

UserProfile.objects.create(
    user=admin,
    job='job',
    gender='M',
    country=Country.objects.get_or_create(name='Italy')[0],
    team=team
);

for challenge in Challenge.objects.all():
    solved = ChallengeSolved.objects.create(
        user=admin.profile,
        challenge=challenge
    )
    solved.created_at = start + timedelta(days=30) * random.random()
    solved.save()

" | python manage.py shell
