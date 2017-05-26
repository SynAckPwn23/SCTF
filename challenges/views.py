import json

from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_417_EXPECTATION_FAILED, HTTP_412_PRECONDITION_FAILED
from rest_framework.viewsets import GenericViewSet

from challenges.models import Challenge, Category, ChallengeSolved, ChallengeFail
from challenges.serializers import ChallengeSolvedSerializer

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Team, UserProfile


def challenges(request):
    categories = Category.objects.all()
    
    user = request.user
    team = user.profile.team
    categories_num_done_user = [
        c.challenges.filter(solved_by=user.profile).distinct().count()
        for c in categories
    ]
    categories_num_done_team = [
        c.challenges.filter(solved_by__team=team).distinct().count()
        for c in categories
    ]

    last_team_solutions = ChallengeSolved.objects\
        .filter(user__team=team)\
        .order_by('-datetime')\
        .all()

    parameters = {
        'team': team,
        'challenges_count': Challenge.objects.count(),
        'categories_num': categories.count(),
        'categories': categories,
        'categories_names': json.dumps([c.name for c in categories]),
        'categories_num_done_user': categories_num_done_user,
        'categories_num_done_team': categories_num_done_team,
        'categories_num_total': [c.challenges.count() for c in categories],
        'last_team_solutions': last_team_solutions,
                
    }

    return render(request, 'challenges/index.html', parameters)


class ChallengeSolvedViewSet(CreateModelMixin, GenericViewSet):
    queryset = ChallengeSolved.objects.all()
    serializer_class = ChallengeSolvedSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        challenge = get_object_or_404(Challenge.objects, pk=serializer.data.get('challenge'))
        key = serializer.data.get('key')
        user = self.request.user
        if user.solved_challenges.filter(pk=challenge.pk).exists():
            return Response('Already solved', status=HTTP_412_PRECONDITION_FAILED)
        if key == challenge.key:
            ChallengeSolved.objects.create(user=user, challenge=challenge)
            return Response('OK')
        ChallengeFail.objects.create(user=user, challenge=challenge)
        return Response('Wrong KEY', status=HTTP_417_EXPECTATION_FAILED)


def scoreboard(request):
    parameters = {
        'teams': Team.objects.all(),
        'user_profiles': UserProfile.objects.ordered(),
    }
    return render(request, 'scoreboard/index.html', parameters)

