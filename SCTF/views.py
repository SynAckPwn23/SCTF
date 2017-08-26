import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from SCTF.consumers import send_message
from SCTF.utils import set_game_duration
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
    }
    return render(request, 'sctf/base.html', parameters)


def _return_back_redirect(request):
    return redirect(request.META.get('HTTP_REFERER', '/'))

@user_passes_test(lambda u: u.is_superuser)
def game_play(request):
    print(config.GAME_STATUS)
    if config.GAME_STATUS == 'SETUP':
        # TODO manage game start
        pass
    elif config.GAME_STATUS == 'PAUSE':
        # TODO manage game resume
        pass
    else:
        return _return_back_redirect(request)

    config.GAME_STATUS = 'PLAY'
    config.GAME_START_DATETIME = datetime.now()
    return _return_back_redirect(request)


@user_passes_test(lambda u: u.is_superuser)
def game_pause(request):
    print(config.GAME_STATUS)
    if config.GAME_STATUS == 'PLAY':
        send_message()
        pass
    else:
        return _return_back_redirect(request)

    config.GAME_STATUS = 'PAUSE'
    set_game_duration(datetime.now() - config.GAME_START_DATETIME)
    return _return_back_redirect(request)


class ChangeGameStaus(APIView):
    # TODO superuser required
    # TODO only post

    def post(self, request, **kwargs):
        status = request.data.get('status')
        if status not in settings.GAME_STATUS_CHOICES_NAMES:
            return Response('Invalid status.', status=400)

        if config.GAME_STATUS == 'FINISH':
            return Response('Game is finished', status=400)

        if status == 'SETUP':
            return Response('Cannot set SETUP', status=400)

        if status == config.GAME_STATUS:
            return Response('Same status', status=400)

        if status == 'PLAY':
            if config.GAME_STATUS == 'SETUP':
                # TODO manage game start
                pass
            elif config.GAME_STATUS == 'PAUSE':
                # TODO manage game resume
                pass

            config.GAME_STATUS = 'PLAY'
            config.GAME_START_DATETIME = datetime.now()

            # TODO manage game
            return Response('Same status', status=200)



