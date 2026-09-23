from rest_framework.routers import DefaultRouter
from .views import (
    ProgramViewSet,
    BlogViewSet,
    TeamMemberViewSet,
    SubscriberViewSet,
)

router = DefaultRouter()
router.register("programs", ProgramViewSet)
router.register("blogs", BlogViewSet)
router.register("team", TeamMemberViewSet)
router.register("subscribers", SubscriberViewSet, basename="subscriber")

urlpatterns = router.urls