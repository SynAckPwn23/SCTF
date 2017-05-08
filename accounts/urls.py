from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^', include('registration.backends.simple.urls')),
    url(r'^', include('registration.auth_urls')),
    url(r'^teams/$', views.index, name='teams'),
    url(r'^team/$', views.team, name='team'),
    url(r'^team/(?P<pk>\w+)$', views.team, name='team'),
]
