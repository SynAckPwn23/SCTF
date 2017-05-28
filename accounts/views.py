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
        'teams': Team.objects.all(),
        'teams_count': Team.objects.count(),

    }

    return render(request, 'accounts/teams.html', parameters)


class CustomRegistrationView(RegistrationView):
    form_class = CustomRegistrationForm
    profile_form = None

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.profile_form = UserProfileForm(request.POST)

        if form.is_valid() and self.profile_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def register(self, form):
        new_user = super(CustomRegistrationView, self).register(form)

        profile = self.profile_form.save(commit=False)
        profile.user = new_user
        profile.save()
        return new_user

    def get_context_data(self, **kwargs):
        kwargs['profile_form'] = self.profile_form or UserProfileForm()
        return super(CustomRegistrationView, self).get_context_data(**kwargs)


def team_detail(request, pk=None):
    # TODO check the more efficent way (order here or not)
    #team = request.user.profile.team if pk is None else Team.objects.get(pk=pk)
    team = Team.objects.ordered().get(pk=pk or request.user.profile.team.pk)

    parameters = {
        'team': team,
        'total_points_count': Challenge.objects.total_points(),
        'time_points': json.dumps(team.score_over_time),
        'category_solved': team.percentage_solved_by_category,
        'last_team_solutions': team.challengesolved_set.order_by('-datetime').all()
    }

    return render(request, 'accounts/team.html', parameters)


def user_detail(request, pk=None):
    user = request.user if pk is None else get_user_model().objects.get(pk=pk)

    solved = user.percentage_solved_by_category()
    categories_names = solved.keys()
    categories_num_done_user = [solved[c] for c in categories_names]

    parameters = {
        'categories_names': json.dumps(categories_names),
        'categories_num_done_user': categories_num_done_user,
        'user_detail_page': user,
        'time_points': json.dumps(user.score_over_time),
    }
    return render(request, 'accounts/user.html', parameters)