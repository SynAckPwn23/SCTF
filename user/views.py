import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from challenges.models import Category


# Create your views here.
@login_required
def index(request, pk=None):
    user = request.user if pk is None else get_user_model().objects.get(pk=pk)

    categories = Category.objects.all()
    categories_num_done_user = [
        c.challenges.filter(solved_by=user).distinct().count()
        for c in categories
    ]

    parameters = {
        'categories_names': json.dumps([c.name for c in categories]),
        'categories_num_done_user': categories_num_done_user,


    }
    return render(request, 'user/index.html', parameters)