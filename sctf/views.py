from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Team
from challenges.models import Challenge


@login_required
def index(request):
    parameters = {
        'users_count': get_user_model().objects.count(),
        'teams_count': Team.objects.count(),
        'challenges_count': Challenge.objects.count(),
    }
    return render(request, 'sctf/base.html', parameters)

