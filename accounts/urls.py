from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('registration.backends.simple.urls')),
    url(r'^', include('registration.auth_urls')),
]

import registration.backends.simple.urls
import registration.auth_urls