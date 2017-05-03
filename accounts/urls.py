from django.conf.urls import include, url

urlpatterns = [
    url('^', include('registration.auth_urls')),
]