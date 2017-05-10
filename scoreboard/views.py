from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Team


@login_required
def index(request):
    parameters = {
        'teams': Team.objects.all(),
        'users': get_user_model().objects.all(),
    }
    return render(request, 'scoreboard/index.html', parameters)

