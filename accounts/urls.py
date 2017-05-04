from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('registration.backends.simple.urls')),
    url(r'^', include('registration.auth_urls')),
]
