from django.http.response import HttpResponseBadRequest
from registration.backends.simple.views import RegistrationView

from accounts.models import Team
from challenges.models import Challenge, ChallengeSolved
from accounts.forms import CustomRegistrationForm, UserProfileForm

import json


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from challenges.models import Category


def index(request):
    parameters = {
        'teams': Team.objects.all()
    }

    return render(request, 'accounts/teams.html', parameters)


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


    def get_context_data(self):
        data = super(CustomRegistrationView, self).get_context_data()
        data.update({
            'profile_form': UserProfileForm()
        })
        return data


def user_detail(request, pk=None):
    user = request.user if pk is None else get_user_model().objects.get(pk=pk)

    categories = Category.objects.all()
    categories_num_done_user = [
        c.challenges.filter(solved_by=user).distinct().count()
        for c in categories
    ]

    parameters = {
        'categories_names': json.dumps([c.name for c in categories]),
        'categories_num_done_user': categories_num_done_user,
        'user_detail_page': user

    }
    return render(request, 'accounts/user.html', parameters)