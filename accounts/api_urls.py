from rest_framework import routers
from .views import TeamCreateViewSet

router = routers.SimpleRouter()
router.register(r'team-create', TeamCreateViewSet, 'team-create')
#router.register(r'team-join', UserTeamRequestViewSet, 'team-join')

urlpatterns = router.urls
