from django.urls import resolve
from rest_framework.reverse import reverse

from django.utils.functional import curry
from django.views.defaults import *

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from accounts.utils import user_without_team


class FilterRequestMiddlewareMixin(MiddlewareMixin):
    redirect_url = ''

    allowed_paths = []
    allowed_views = []

    def base_filter(self, request):
        return False
        return 'admin' not in request.path and \
               'accounts/registration' not in request.path and \
               (request.path in self.allowed_paths and\
                resolve(request.path_info).url_name in self.allowed_views)

    def custom_filter(self, request):
        return True

    def filter(self, request):
        return self.base_filter(request) and self.custom_filter(request)

    def response(self, request):
        return HttpResponseRedirect(self.redirect_url)

    def process_request(self, request):
        print(request)
        if self.filter(request):
            print('nopass middleware')
            return self.response(request)
        print('pass middleware')

class LoginRequiredMiddleware(FilterRequestMiddlewareMixin):

    redirect_url = reverse('auth_login')

    def custom_filter(self, request):
        return not request.user.is_authenticated()


class LoggedInUserWithoutProfileMiddleware(FilterRequestMiddlewareMixin):
    allowed_paths = [
        reverse('auth_logout')
    ]

    def custom_filter(self, request):
        return not hasattr(request.user, 'profile')

    def response(self, request):
        return curry(server_error,
                     template_name='accounts/500_no_profile.html')(request)


class LoggedInUserWithoutTeamMiddleware(FilterRequestMiddlewareMixin):
    redirect_url = reverse('no_team')

    allowed_paths = [
        reverse('no_team'),
        reverse('api-accounts:team-create-list'),
        reverse('user_team_request_create'),
    ]

    allowed_views = [
        'user_team_request_delete'
    ]

    def custom_filter(self, request):
        print(resolve(request.path_info).url_name)
        return user_without_team(request.user)
