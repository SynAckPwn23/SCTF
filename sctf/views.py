from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    parameters = {
        'users_count': get_user_model().objects.count(),
    }
    return render(request, 'base.html', parameters)

