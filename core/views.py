from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Program, Blog, TeamMember
from .serializers import ProgramSerializer, BlogSerializer, TeamMemberSerializer

@extend_schema_view(
    list=extend_schema(description="Get a list of all programs"),
    retrieve=extend_schema(description="Get a specific program by ID")
)
class ProgramViewSet(ReadOnlyModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

@extend_schema_view(
    list=extend_schema(description="Get a list of all blog posts"),
    retrieve=extend_schema(description="Get a specific blog post by ID")
)
class BlogViewSet(ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

@extend_schema_view(
    list=extend_schema(description="Get a list of all team members"),
    retrieve=extend_schema(description="Get a specific team member by ID")
)
class TeamMemberViewSet(ReadOnlyModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer