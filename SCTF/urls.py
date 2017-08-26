from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include
from rest_framework import routers
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^challenges/', include('challenges.urls')),

    url(r'^admin/game_start/', views.game_play, name='admin_game_start'),
    url(r'^admin/game_pause/', views.game_pause, name='admin_game_pause'),

    url(r'^game_paused/$', views.game_paused_view, name='game_paused_view'),
    url(r'^game_stopped/$', views.game_stopped_view, name='game_stopped_view'),

    url(r'^admin/game_end/', views.game_end, name='admin_game_end'),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^tinymce/', include('tinymce.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

router = routers.SimpleRouter()

# Include REST
urlpatterns.append(url(r'^api/', include(router.urls)))

urlpatterns.append(url(r'^api/challenges/',
                       include('challenges.api_urls', namespace='api-challenge')))


urlpatterns.append(url(r'^api/users/',
                       include('accounts.api_urls', namespace='api-users')))

