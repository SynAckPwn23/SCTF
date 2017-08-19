from rest_framework.reverse import reverse

from django.utils.functional import curry
from django.views.defaults import *

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from accounts.utils import user_without_team


class FilterRequestMiddlewareMixin(MiddlewareMixin):
    redirect_url = ''

    allowed_paths = []

    def base_filter(self, request):
        return 'admin' not in request.path and \
               'accounts/registration' not in request.path and \
               request.path not in self.allowed_paths

    def custom_filter(self, request):
        return True

    def filter(self, request):
        return self.base_filter(request) and self.custom_filter(request)

    def response(self, request):
        return HttpResponseRedirect(self.redirect_url)

    def process_request(self, request):
        if self.filter(request):
            return self.response(request)


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
        reverse('no_team'), reverse('api-accounts:team-list')
    ]

    def custom_filter(self, request):
        print(self.allowed_paths)
        return user_without_team(request.user)
