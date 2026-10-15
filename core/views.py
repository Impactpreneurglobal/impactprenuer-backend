from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import (
    Program, Blog, TeamMember, Subscriber,
    ServiceRequest, ContactMessage, CommunityApplication,
)
from .serializers import (
    ProgramSerializer, BlogSerializer, TeamMemberSerializer, SubscriberSerializer,
    ServiceRequestSerializer, ContactMessageSerializer, CommunityApplicationSerializer,
)
from .emails import send_form_emails, send_welcome_email


# ── Existing content viewsets ─────────────────────────────────
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
        if self.action == "create":
            return [AllowAny()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        instance = serializer.save()
        send_welcome_email(instance)


# ── Form viewset base ─────────────────────────────────────────
class _PublicCreateAdminReadViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """
    Public POST, admin-only GET. Subclass and override:
      - queryset
      - serializer_class
      - form_name (human readable)
      - build_details(instance) -> dict
      - submitter_email_field / submitter_name_field
    """
    form_name = "Form"
    submitter_email_field = "email"
    submitter_name_field = "full_name"

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAdminUser()]

    def build_details(self, instance):
        # default: dump every field except created_at
        return {
            f.name: getattr(instance, f.name)
            for f in instance._meta.fields
            if f.name != "created_at"
        }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # send confirmation + team notification
        send_form_emails(
            form_name=self.form_name,
            submitter_email=getattr(instance, self.submitter_email_field),
            submitter_name=getattr(instance, self.submitter_name_field, "there"),
            details=self.build_details(instance),
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


# ── New form viewsets ─────────────────────────────────────────
@extend_schema_view(
    create=extend_schema(description="Submit a service request"),
    list=extend_schema(description="List all service requests (admin only)"),
)
class ServiceRequestViewSet(_PublicCreateAdminReadViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    form_name = "Service Request"
    submitter_name_field = "full_name"


@extend_schema_view(
    create=extend_schema(description="Submit a contact message"),
    list=extend_schema(description="List all contact messages (admin only)"),
)
class ContactMessageViewSet(_PublicCreateAdminReadViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    form_name = "Contact Message"
    submitter_name_field = "full_name"


@extend_schema_view(
    create=extend_schema(description="Submit a community application"),
    list=extend_schema(description="List all community applications (admin only)"),
)
class CommunityApplicationViewSet(_PublicCreateAdminReadViewSet):
    queryset = CommunityApplication.objects.all()
    serializer_class = CommunityApplicationSerializer
    form_name = "Community Application"
    submitter_name_field = "full_name"