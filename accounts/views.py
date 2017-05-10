from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Team
from challenges.models import Challenge



@login_required
def index(request):
    parameters = {
        'teams': Team.objects.all()
    }

    return render(request, 'accounts/teams.html', parameters)


@login_required
def team(request, pk=None):
    team = request.user.profile.team if pk is None else Team.objects.get(pk=pk)
    parameters = {
        'team': team,
        'total_points_count': Challenge.objects.total_points(),
        'teams_count': Team.objects.count(),


    }

    return render(request, 'accounts/team.html', parameters)

