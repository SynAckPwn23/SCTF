from collections import defaultdict

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from registration.backends.simple.views import RegistrationView

from accounts.models import Team, UserProfile
from challenges.models import Challenge, ChallengeSolved, Category
from accounts.forms import CustomRegistrationForm, UserProfileForm

import json


import django.contrib.auth.views


@login_required
def index(request):
    parameters = {
        'teams': Team.objects.all()
    }

    return render(request, 'accounts/teams.html', parameters)


@login_required
def team(request, pk=None):
    team = request.user.profile.team if pk is None else Team.objects.get(pk=pk)

    time_points = []
    points = 0
    for solved in ChallengeSolved.objects.filter(user__profile__team=team).distinct().order_by('datetime'):
        points += solved.challenge.points
        time_points.append([int(solved.datetime.timestamp())*1000, points])

    category_solved = {
        c.name: int(team.solved_challenges.filter(category=c).count() / (c.challenges.count() or 1) * 100)
        for c in Category.objects.all()
    }

    parameters = {
        'team': team,
        'total_points_count': Challenge.objects.total_points(),
        'teams_count': Team.objects.count(),

        'time_points': json.dumps(time_points),
        'category_solved': category_solved
    }

    return render(request, 'accounts/team.html', parameters)



class CustomRegistrationView(RegistrationView):
    form_class = CustomRegistrationForm

    def register(self, form):
        profile_form = UserProfileForm(self.request.POST)
        if not profile_form.is_valid():
            raise HttpResponseBadRequest()
        new_user = super(CustomRegistrationView, self).register(form)

        profile = profile_form.save(commit=False)
        profile.user = new_user
        profile.save()
        return new_user

