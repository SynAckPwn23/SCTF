from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Team


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
        'team': team
    }

    return render(request, 'accounts/team.html', parameters)

