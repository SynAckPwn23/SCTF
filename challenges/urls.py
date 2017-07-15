from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^challenges/$', views.challenges_categories, name='challenges_categories'),
    url(r'^category/(?P<category_pk>\w+)/$', views.challenges_category, name='challenges_category'),
    url(r'^challenges_solved/$', views.challenges_solved, name='challenges_solved'),
    url(r'^teams_ranking/$', views.teams_ranking, name='teams_ranking'),
    url(r'^users_ranking/$', views.users_ranking, name='users_ranking'),
]

