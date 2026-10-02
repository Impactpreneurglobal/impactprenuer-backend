from rest_framework import serializers
from .models import Program, Blog, TeamMember, Subscriber


class ProgramSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Program
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)   # NEW

    class Meta:
        model = Blog
        fields = "__all__"


class TeamMemberSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = TeamMember
        fields = "__all__"


# ── NEW ─
class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ["id", "email", "created_at"]
        read_only_fields = ["id", "created_at"]
