from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from sctf.models import Team


@login_required
def index(request):
    parameters = {
        'users_count': get_user_model().objects.count(),
        'teams_count': Team.objects.count(),
    }
    return render(request, 'base.html', parameters)

