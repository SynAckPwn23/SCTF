from rest_framework import routers
from .views import UserTeamRequestViewSet

router = routers.SimpleRouter()
router.register(r'user-team-request', UserTeamRequestViewSet, 'user-team-request')

urlpatterns = router.urls