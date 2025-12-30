from rest_framework.routers import DefaultRouter
from .views import ProgramViewSet, BlogViewSet, TeamMemberViewSet

router = DefaultRouter()
router.register("programs", ProgramViewSet)
router.register("blogs", BlogViewSet)
router.register("team", TeamMemberViewSet)

urlpatterns = router.urls
