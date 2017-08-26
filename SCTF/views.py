import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.shortcuts import render

from SCTF.utils import game_duration
from accounts.models import Team
from challenges.models import Challenge
from cities_light.models import Country
from constance import config


def index(request):
    user = request.user

    countries = Country.objects\
        .annotate(num_user=Count('userprofile'))\
        .filter(num_user__gt=0)

    parameters = {
        'users_count': get_user_model().objects.count(),
        'teams_count': Team.objects.count(),
        'challenges_count': Challenge.objects.count(),
        'total_points_count': Challenge.objects.total_points(),
        'user_points_count': user.profile.total_points,
        'countries_users': json.dumps({c.code2.lower(): c.num_user for c in countries}),
        'config': config,
        'game_end_datetime': config.GAME_START_DATETIME + game_duration()
    }
    return render(request, 'sctf/base.html', parameters)


@user_passes_test(lambda u: u.is_superuser)
def game_play(request):
    from datetime import datetime
    # TODO check status
    config.GAME_START_DATETIME = datetime.now()
    config.GAME_STATUS = 'PLAY'


@user_passes_test(lambda u: u.is_superuser)
def game_pause(request):
    pass