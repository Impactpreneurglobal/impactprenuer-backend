from django.contrib import admin
from .models import (
    ServiceRequest, ContactMessage, CommunityApplication,
    Program, Blog, TeamMember, Subscriber,
)
from django.contrib import admin


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date", "created_at")
    list_filter = ("author", "date", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "title")
    search_fields = ("name", "title", "bio")


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)
    ordering = ("-created_at",)

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "service", "country", "created_at")
    list_filter = ("service", "stage", "country", "created_at")
    search_fields = ("full_name", "email", "organization_name", "help_description")
    ordering = ("-created_at",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "created_at")
    search_fields = ("full_name", "email", "subject", "message")
    ordering = ("-created_at",)


@admin.register(CommunityApplication)
class CommunityApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "country", "created_at")
    list_filter = ("country", "created_at")
    search_fields = ("full_name", "email", "organization_name", "building_description")
    ordering = ("-created_at",)