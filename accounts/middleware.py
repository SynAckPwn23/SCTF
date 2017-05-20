from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from rest_framework.reverse import reverse


class LoggedInUserWithoutProfileMiddleware(MiddlewareMixin):
    redirect_url = reverse('no_profile')
    def process_request(self, request):
        if request.user.is_authenticated() and \
                not hasattr(request.user, 'profile') and \
                request.path != self.redirect_url:
            return HttpResponseRedirect(self.redirect_url)


class LoggedInUserWithoutTeamMiddleware(MiddlewareMixin):
    redirect_url = reverse('no_team')

    allowed_paths = [
        redirect_url,
        reverse('no_profile'),
        # TODO set pages allowed to users without team (ie user profile)
    ]

    def process_request(self, request):
        if request.path in self.allowed_paths:
            return
        if request.user.is_authenticated() and request.user.profile.team is None:
            return HttpResponseRedirect(self.redirect_url)