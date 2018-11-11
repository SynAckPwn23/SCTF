from django.conf.urls import include, url
from django.views.generic import TemplateView
from accounts.views import CustomRegistrationView
from . import views

urlpatterns = [
    url(r'^registration/register/$',
        CustomRegistrationView.as_view(),
        name='registration_register'
    ),

    url(r'^registration/', include('django_registration.backends.one_step.urls')),
    url(r'^registration/', include('django.contrib.auth.urls')),
    url(r'^teams/$', views.index, name='teams'),
    url(r'^team/$', views.team_detail, name='team'),
    url(r'^team/(?P<pk>\w+)$', views.team_detail, name='team'),
    url(r'^user/$', views.user_detail, name='user'),
    url(r'^user/(?P<pk>\w+)$', views.user_detail, name='user'),
    url(r'^user/update/$', views.UserProfileUpdateView.as_view(), name='user_update'),

    url(r'^no-team/$', views.no_team_view, name='no_team'),

    url(r'^team/admin/$', views.TeamAdminView.as_view(), name='team_admin'),

    url(r'^team/create/$', views.TeamCreateView.as_view(), name='user_team_create'),

    url(r'^team/request/create/$',
        views.UserTeamRequestCreate.as_view(), name='user_team_request_create'),

    url(r'^team/request/delete/(?P<pk>\w+)/$',
        views.UserTeamRequestDelete.as_view(), name='user_team_request_delete'),

    url(r'^team/admin/request/(?P<pk>\w+)/$',
        views.UserTeamRequestManage.as_view(), name='user_team_request_manage'),

    url(r'^no-profile/$',
        TemplateView.as_view(template_name="accounts/no_profile.html"),
        name='no_profile'
    ),

]
