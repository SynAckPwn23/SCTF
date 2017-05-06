from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.db.models import Sum

from accounts.models import Team
from challenges.models import Challenge




@login_required
def index(request):
    parameters = {
        'users_count': get_user_model().objects.count(),
        'teams_count': Team.objects.count(),
        'challenges_count': Challenge.objects.count(),
        'points_count': Challenge.objects.aggregate(Sum('points')).values(),
    }
    return render(request, 'sctf/base.html', parameters)

