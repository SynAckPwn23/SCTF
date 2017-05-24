#!/bin/bash

# Locations
python manage.py loaddata locations.json


# Users Data
python manage.py loadtestdata accounts.Team:10 -u accounts.fixtures.autofixtures.TeamAutoFixture
python manage.py loadtestdata auth.User:50 -u accounts.fixtures.autofixtures.UserAutoFixture
python manage.py loadtestdata accounts.UserProfile:50 -u accounts.fixtures.autofixtures.UserProfileAutoFixture


# Challenges Categories
python manage.py loaddata categories.json


# Challenges
