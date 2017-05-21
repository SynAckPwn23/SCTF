from autofixture import generators, register, AutoFixture
from django.contrib.auth import get_user_model

from accounts.models import UserProfile, Team
from django.contrib.auth.hashers import make_password

from accounts.fixtures.autofixtures_data import user_first_names, user_last_names, team_names, user_usernames


class UserAutoFixture(AutoFixture):
    field_values = {
        'username': generators.ChoicesGenerator(choices=user_usernames),
        'password': generators.StaticGenerator(make_password('demo')),
        'first_name': generators.ChoicesGenerator(choices=user_first_names),
        'last_name': generators.ChoicesGenerator(choices=user_last_names),
    }


class TeamAutoFixture(AutoFixture):
    field_values = {
        'name': generators.ChoicesGenerator(choices=team_names),
    }

register(get_user_model(), UserAutoFixture)
register(UserProfile, AutoFixture)
register(Team, TeamAutoFixture)

