

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include
from rest_framework import routers

urlpatterns = [
    url(r'^', include('sctf.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^challenges/', include('challenges.urls')),
    url(r'^scoreboard/', include('scoreboard.urls')),
    url(r'^user/', include('user.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

router = routers.SimpleRouter()

# Include REST
urlpatterns.append(url(r'^api/', include(router.urls)))

urlpatterns.append(url(r'^api/challenges/',
                       include('challenges.api_urls', namespace='api-challenge')))