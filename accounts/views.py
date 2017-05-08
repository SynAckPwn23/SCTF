from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Team


@login_required
def index(request):
    parameters = {
        'teams': Team.objects.all()
    }

    return render(request, 'accounts/teams.html', parameters)

