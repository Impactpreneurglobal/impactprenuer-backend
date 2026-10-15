from rest_framework.routers import DefaultRouter
from .views import (
    ProgramViewSet, BlogViewSet, TeamMemberViewSet, SubscriberViewSet,
    ServiceRequestViewSet, ContactMessageViewSet, CommunityApplicationViewSet,
)

router = DefaultRouter()
router.register("programs", ProgramViewSet)
router.register("blogs", BlogViewSet)
router.register("team", TeamMemberViewSet)
router.register("subscribers", SubscriberViewSet, basename="subscriber")
router.register("service-requests", ServiceRequestViewSet, basename="service-request")
router.register("contact", ContactMessageViewSet, basename="contact")
router.register("applications", CommunityApplicationViewSet, basename="application")

urlpatterns = router.urls