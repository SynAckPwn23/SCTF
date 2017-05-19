from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^challenges/$', views.challenges, name='challenges'),
    url(r'^scoreboard/$', views.scoreboard, name='scoreboard'),
]

