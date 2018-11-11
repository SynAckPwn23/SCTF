import json
from builtins import super

from django.http import HttpResponseForbidden
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
# from registration.backends.simple.views import RegistrationView
from django_registration.views import RegistrationView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from accounts.models import Team, UserTeamRequest, User
from accounts.forms import CustomRegistrationForm, UserProfileForm, UserTeamRequestCreateForm, TeamCreateForm
from accounts.serializers import UserTeamRequestListSerializer
from accounts.utils import user_without_team
from challenges.models import Challenge
from challenges.models import Category


def index(request):
    return render(request, 'accounts/teams.html', {
        'teams': Team.objects.all(),
        'teams_count': Team.objects.count(),
    })


class CustomRegistrationView(RegistrationView):
    form_class = CustomRegistrationForm
    profile_form = None
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.profile_form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid() and self.profile_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def register(self, form):
        # new_user = super(CustomRegistrationView, self).register(form)
        new_user = form.save()
        profile = self.profile_form.save(commit=False)
        profile.user = new_user
        profile.save()
        return new_user

    def get_context_data(self, **kwargs):
        kwargs['profile_form'] = self.profile_form or UserProfileForm()
        return super(CustomRegistrationView, self).get_context_data(**kwargs)


def team_detail(request, pk=None):
    user = request.user
    team = user.profile.team if pk is None else Team.objects.get(pk=pk)

    categories = Category.objects.all()
    categories_num_done_user = [
        c.challenges.filter(solved_by=user.profile).distinct().count()
        for c in categories
    ]
    categories_num_done_team = [
        c.challenges.filter(solved_by__team=team).distinct().count()
        for c in categories
    ]

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


def no_team_view(request, create_form=TeamCreateForm(), join_form=UserTeamRequestCreateForm()):
    # TODO: use permissions
    if not user_without_team(request.user):
        return redirect('index')

    pending_request = request.user.userteamrequest_set.pending().first()
    if pending_request:
        return render(request, 'accounts/pending_request.html', dict(join_request=pending_request))

    return render(request, 'accounts/no_team.html', dict(
        team_create_form=create_form,
        team_join_form=join_form,
        teams=Team.objects.all(),
        join_request_rejected=request.user.userteamrequest_set.rejected().exists()
    ))


class NoTeamPostView(CreateView):
    success_url = '/'
    form_name = None

    # TODO: use permissions
    def get(self, *args, **kwargs):
        return redirect('no_team')

    def form_invalid(self, form):
        return no_team_view(self.request, **{self.form_name: form})


class TeamCreateView(NoTeamPostView):
    form_class = TeamCreateForm
    success_url = reverse_lazy('index')
    form_name = 'create_form'

    def form_valid(self, form):
        team=form.save(commit=False)
        team.created_by=self.request.user
        team.save()
        team.created_by.profile.team = team
        team.created_by.profile.save()
        return super(TeamCreateView, self).form_valid(form)


class UserTeamRequestCreate(NoTeamPostView):
    form_class = UserTeamRequestCreateForm
    form_name = 'join_form'

    def get_form(self):
        return UserTeamRequestCreateForm(data=dict(
            user=self.request.user.pk,
            team=self.request.POST.get('team')))


class TeamAdminView(TemplateView):
    template_name = 'accounts/team_admin.html'

    # TODO: use permissions
    def get(self, request, *args, **kwargs):
        if not self.request.user.created_team.first():
            return redirect('index')
        return super(TeamAdminView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return dict(
            join_requests=self.request.user.created_team.first().userteamrequest_set.order_by('-datetime')
        )


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


class UserTeamRequestDelete(DeleteView):
    model = UserTeamRequest
    success_url = reverse_lazy('no_team')

    # TODO: use permissions
    def dispatch(self, request, *args, **kwargs):
        r = self.get_object()
        if r.user != request.user and r.team.created_by != request.user:
            return HttpResponseForbidden()
        return super(UserTeamRequestDelete, self).dispatch(request, *args, **kwargs)


class UserTeamRequestManage(UpdateView):
    model = UserTeamRequest
    fields = ['status']
    success_url = reverse_lazy('team_admin')
    http_method_names = ['post']

    # TODO: use permissions
    def post(self, request, *args, **kwargs):
        r = self.get_object()
        if not r.team.created_by == request.user:
            return Response('You are not team admin', status=403)
        if r.status != 'P':
            return Response('Not yet pending', status=400)
        return super(UserTeamRequestManage, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super(UserTeamRequestManage, self).form_valid(form)
        if self.object.status == 'A':
            self.object.user.profile.team = self.object.team
            self.object.user.profile.save()
        return response


class UserTeamRequestViewSet(ModelViewSet):
    serializer_class = UserTeamRequestListSerializer

    def get_queryset(self):
        return UserTeamRequest.objects.filter(team__created_by=self.request.user)


class UserRequestHTMLTable(TeamAdminView, TemplateView):
    template_name = 'accounts/team_admin_requests_list.html'
