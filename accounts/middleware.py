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

    def process_request(self, request):
        if not request.user.is_authenticated() and 'login' not in request.path:
            return HttpResponseRedirect(reverse('auth_login'))


class LoggedInUserWithoutTeamMiddleware(MiddlewareMixin):
    redirect_url = reverse('no_team')

    disallowed_paths = [
        reverse('no_profile'),
        reverse('no_team'),
        # TODO set pages allowed to users without team (ie: manage user profile)
    ]

    def process_request(self, request):
        if request.path in self.disallowed_paths and \
                request.user.is_authenticated() and \
                request.user.profile.team is None:
            return HttpResponseRedirect(self.redirect_url)