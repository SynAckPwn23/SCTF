from django.conf.urls import include, url
from registration.views import RegistrationView

from accounts.forms import CustomRegistrationForm
from accounts.views import CustomRegistrationView
from . import views

urlpatterns = [
    url(r'^register/$',
        CustomRegistrationView.as_view(),
        name='registration_register'
    ),
    url(r'^', include('registration.backends.simple.urls')),
    url(r'^', include('registration.auth_urls')),
    url(r'^teams/$', views.index, name='teams'),
    url(r'^team/$', views.team, name='team'),
    url(r'^team/(?P<pk>\w+)$', views.team, name='team'),
    url(r'^user/$', views.index, name='user'),
    url(r'^user/(?P<pk>\w+)$', views.index, name='user'),
]
