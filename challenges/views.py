from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from challenges.models import Challenge, Category


@login_required
def index(request):
    parameters = {
        'challenges': Challenge.objects.all(),
        'categories': Category.objects.all()
    }

    return render(request, 'challenges/index.html', parameters)

