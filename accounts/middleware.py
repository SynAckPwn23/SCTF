from rest_framework.reverse import reverse

from django.utils.functional import curry
from django.views.defaults import *

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class LoggedInUserWithoutProfileMiddleware(MiddlewareMixin):
    redirect_url = reverse('no_profile')

    def process_request(self, request):
        if request.user.is_authenticated() and \
                not hasattr(request.user, 'profile') and \
                request.path not in (self.redirect_url, reverse('auth_logout')):
            handler500 = curry(server_error, template_name='accounts/500_no_profile.html')
            return handler500(request)


class LoginRequiredMiddleware(MiddlewareMixin):

    allowed_paths = [
    ]

    def process_request(self, request):
        if not request.user.is_authenticated() and \
                'admin' not in request.path and \
                'accounts/registration' not in request.path and \
                request.path not in self.allowed_paths:
            return HttpResponseRedirect(reverse('auth_login'))


class LoggedInUserWithoutTeamMiddleware(MiddlewareMixin):
    redirect_url = reverse('no_team')

    allowed_paths = [
        reverse('no_team')
    ]

    def process_request(self, request):
        if request.user.is_authenticated() and \
                'admin' not in request.path and \
                'accounts/registration' not in request.path and \
                request.path not in self.allowed_paths:
            return HttpResponseRedirect(self.redirect_url)

