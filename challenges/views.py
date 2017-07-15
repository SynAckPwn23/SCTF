import json

from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_417_EXPECTATION_FAILED, HTTP_412_PRECONDITION_FAILED
from rest_framework.viewsets import GenericViewSet

from challenges.models import Challenge, Category, ChallengeSolved, ChallengeFail
from challenges.serializers import ChallengeSolvedSerializer

from django.shortcuts import render

from accounts.models import Team, UserProfile
from SCTF.consumers import send_message


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
        if user.profile.solved_challenges.filter(pk=challenge.pk).exists():
            return Response('Already solved', status=HTTP_412_PRECONDITION_FAILED)
        if key == challenge.key:
            ChallengeSolved.objects.create(user=user.profile, challenge=challenge)
            send_message(json.dumps({
                'event': 'CHALLENGE_SOLVED',
                'user': user.pk,
                'team': user.profile.team.pk,
                'challenge': challenge.pk,
            }))
            return Response('OK')
        ChallengeFail.objects.create(user=user.profile, challenge=challenge)
        return Response('Wrong KEY', status=HTTP_417_EXPECTATION_FAILED)


def teams_ranking(request):
    parameters = {
        'teams': Team.objects.ordered(),
    }
    return render(request, 'scoreboard/teams_ranking.html', parameters)


def users_ranking(request):
    parameters = {
        'user_profiles': UserProfile.objects.ordered(),
    }
    return render(request, 'scoreboard/users_ranking.html', parameters)


def challenges_solved(request):
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

    last_team_solutions = ChallengeSolved.objects \
        .filter(user__team=team) \
        .order_by('-datetime') \
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

    return render(request, 'challenges/challenges_solved.html', parameters)

