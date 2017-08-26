from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


from constance import config


class FilterRequestByGameStateMiddlewareMixin(MiddlewareMixin):

    def process_request(self, request):
        if 'challenge' in request.path and config.GAME_STATUS != 'PLAY':
            return HttpResponseRedirect('/')