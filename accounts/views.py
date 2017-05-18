from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Team
from challenges.models import Challenge, ChallengeSolved

import json


@login_required
def index(request):
    parameters = {
        'teams': Team.objects.all()
    }

    return render(request, 'accounts/teams.html', parameters)


@login_required
def team(request, pk=None):
    team = request.user.profile.team if pk is None else Team.objects.get(pk=pk)




    time_points = defaultdict(lambda : 0)
    for solved in ChallengeSolved.objects.filter(user__profile__team=team):
        time_points[solved.datetime.timestamp()] += solved.challenge.points

    parameters = {
        'team': team,
        'total_points_count': Challenge.objects.total_points(),
        'teams_count': Team.objects.count(),

        'time_points': json.dumps(sorted(time_points.items())),

    }

    return render(request, 'accounts/team.html', parameters)

