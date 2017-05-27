import os
import random
from datetime import timedelta, datetime
from io import BytesIO
from itertools import repeat, cycle

import requests
from autofixture import generators, register, AutoFixture
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from accounts.models import UserProfile, Team
from django.contrib.auth.hashers import make_password

from accounts.fixtures.autofixtures_data import user_first_names, user_last_names, team_names, user_usernames
from challenges.models import Challenge, ChallengeSolved


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


teams = cycle(iter(Team.objects.exclude(name='admin')))

class UserProfileAutoFixture(AutoFixture):

    field_values = {
        'team': generators.CallableGenerator(lambda *args, **kwargs: next(teams))
    }

    def post_process_instance(self, instance, commit=True):
        # created date
        instance.created_at = now() - timedelta(days=30)

        # solved challenges
        for challenge in Challenge.objects.filter(pk__gt=instance.pk):
            solved = ChallengeSolved.objects.create(
                user=instance,
                challenge=challenge
            )
            start = instance.created_at
            solved.datetime = start + (now() - start) * random.random()
            solved.save()


        # random image
        gender = 'men' if instance.gender == 'M' else 'women'
        image_url = 'https://randomuser.me/api/portraits/{}/{}.jpg'.format(gender, instance.id)
        try:
            response = requests.get(image_url)
        except requests.HTTPError as e:
            print(e)
            return instance

        instance.image.save(
            os.path.basename('image_{}.jpg'.format(instance.id)),
            BytesIO(response.content)
        )

        if commit:
            instance.save()

        return instance


register(get_user_model(), UserAutoFixture)
register(UserProfile, UserProfileAutoFixture)
register(Team, TeamAutoFixture)

