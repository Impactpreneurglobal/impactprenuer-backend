from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Program, Blog, TeamMember, Subscriber
from .serializers import (
    ProgramSerializer,
    BlogSerializer,
    TeamMemberSerializer,
    SubscriberSerializer,
)


@extend_schema_view(
    list=extend_schema(description="Get a list of all programs"),
    retrieve=extend_schema(description="Get a specific program by ID"),
)
class ProgramViewSet(ReadOnlyModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


@extend_schema_view(
    list=extend_schema(description="Get a list of all blog posts"),
    retrieve=extend_schema(description="Get a specific blog post by ID"),
)
class BlogViewSet(ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


@extend_schema_view(
    list=extend_schema(description="Get a list of all team members"),
    retrieve=extend_schema(description="Get a specific team member by ID"),
)
class TeamMemberViewSet(ReadOnlyModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer


# ── NEW 
@extend_schema_view(
    create=extend_schema(description="Subscribe an email address to the newsletter"),
    list=extend_schema(description="List all subscribers (admin only)"),
)
class SubscriberViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    def get_permissions(self):
        # Anyone can subscribe (POST). Only admins can list/retrieve.
        if self.action == "create":
            return [AllowAny()]
        return [IsAdminUser()]
