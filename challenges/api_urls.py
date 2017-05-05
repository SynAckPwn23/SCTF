from rest_framework import routers
from .views import ChallengeSolvedViewSet

router = routers.SimpleRouter()
router.register(r'solve-challenge', ChallengeSolvedViewSet, 'solve-challenge')

urlpatterns = router.urls