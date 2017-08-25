#from rest_framework import routers
from django.conf.urls import url

from .views import UserRequestHTMLTable

'''
router = routers.SimpleRouter()
router.register(r'user-team-request', UserTeamRequestViewSet, 'user-team-request')

urlpatterns = router.urls + [
    
]
'''
urlpatterns = [url('user-team-request', UserRequestHTMLTable.as_view())]
