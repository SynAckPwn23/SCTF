import json
from builtins import super

from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, CreateView
from django.views.generic.list import ListView
from registration.backends.simple.views import RegistrationView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from accounts.models import Team, UserTeamRequest
from accounts.permissions import UserWithoutTeamOrAdmin
from accounts.forms import CustomRegistrationForm, UserProfileForm
from accounts.utils import user_without_team
from challenges.models import Challenge, ChallengeSolved
from challenges.models import Category
from challenges.serializers import TeamSerializer, UserTeamRequestSerializer


def index(request):
    return render(request, 'accounts/teams.html', {
        'teams': Team.objects.all(),
        'teams_count': Team.objects.count(),
    })


class CustomRegistrationView(RegistrationView):
    form_class = CustomRegistrationForm
    profile_form = None

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.profile_form = UserProfileForm(request.POST, request.FILES)
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
    
    categories = Category.objects.all()

    user = request.user
    team = user.profile.team
    categories_num_done_user = [
        c.challenges.filter(solved_by=user.profile).distinct().count()
        for c in categories
    ]
    categories_num_done_team = [
        c.challenges.filter(solved_by__team=team).distinct().count()
        for c in categories
    ]

    last_team_solutions = ChallengeSolved.objects \
        .filter(user__team=team) \
        .order_by('-datetime') \
        .all()

    parameters = {
        'team': team,
        'total_points_count': Challenge.objects.total_points(),
        'time_points': json.dumps(team.score_over_time),
        'category_solved': team.percentage_solved_by_category,
        'last_team_solutions': team.challengesolved_set.order_by('-datetime').all(),

        'categories_names': json.dumps([c.name for c in categories]),
        'categories_num_done_user': categories_num_done_user,
        'categories_num_done_team': categories_num_done_team,
        'categories_num_total': [c.challenges.count() for c in categories],
    }

    return render(request, 'accounts/team.html', parameters)


class TeamCreateViewSet(CreateModelMixin, GenericViewSet):
    queryset = Team.objects.all()
    permission_classes = (IsAuthenticated, UserWithoutTeamOrAdmin)
    serializer_class = TeamSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)
        if not user.is_superuser:
            user.profile.team = serializer.instance
            user.profile.save()


class NoTeamView(TemplateView):
    template_name = 'accounts/no_team.html'

    def get(self, request, *args, **kwargs):
        if not user_without_team(request.user):
            return redirect('index')
        return super(NoTeamView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return dict(teams=Team.objects.all())




def user_detail(request, pk=None):
    user = request.user if pk is None else get_user_model().objects.get(pk=pk)

    solved = user.profile.percentage_solved_by_category
    categories_names = list(solved.keys())
    categories_num_done_user = [solved[c] for c in categories_names]

    parameters = {
        'categories_names': json.dumps(categories_names),
        'categories_num_done_user': categories_num_done_user,
        'user_detail_page': user,
        'time_points': json.dumps(user.profile.score_over_time),
    }
    return render(request, 'accounts/user.html', parameters)


def user_detail_test(request, pk=None):
    user = request.user if pk is None else get_user_model().objects.get(pk=pk)

    solved = user.profile.percentage_solved_by_category
    categories_names = list(solved.keys())
    categories_num_done_user = [solved[c] for c in categories_names]

    parameters = {
        'categories_names': json.dumps(categories_names),
        'categories_num_done_user': categories_num_done_user,
        'user_detail_page': user,
        'time_points': json.dumps(user.profile.score_over_time),
    }
    return render(request, 'accounts/user_test.html', parameters)


class UserTeamRequestViewSet(ModelViewSet):
    queryset = UserTeamRequest.objects.none()
    permission_classes = (IsAuthenticated, UserWithoutTeamOrAdmin)
    serializer_class = UserTeamRequestSerializer

    def get_queryset(self):
        return self.request.user.team.userteamrequest_set.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

