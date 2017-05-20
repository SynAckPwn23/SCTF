from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from rest_framework.reverse import reverse

from django.utils.functional import curry
from django.views.defaults import *



class LoggedInUserWithoutProfileMiddleware(MiddlewareMixin):
    redirect_url = reverse('no_profile')

    def process_request(self, request):
        if request.user.is_authenticated() and \
                not hasattr(request.user, 'profile') and \
                request.path != self.redirect_url:
            handler500 = curry(server_error, template_name='accounts/500_no_profile.html')
            return handler500(request)


class LoggedInUserWithoutTeamMiddleware(MiddlewareMixin):
    redirect_url = reverse('no_team')

    allowed_paths = [
        reverse('no_profile'),
        reverse('no_team'),
        # TODO set pages allowed to users without team (ie: manage user profile)
    ]

    def process_request(self, request):
        if request.path not in self.allowed_paths and \
                request.user.is_authenticated() and \
                request.user.profile.team is None:
            return HttpResponseRedirect(self.redirect_url)