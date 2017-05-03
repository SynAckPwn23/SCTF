from django.conf.urls import include, url

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^', include('registration.auth_urls')),
]