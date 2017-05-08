from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^', include('registration.backends.simple.urls')),
    url(r'^', include('registration.auth_urls')),
    url(r'^teams/$', views.index, name='teams'),
]
