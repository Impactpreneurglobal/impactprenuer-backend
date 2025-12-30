from django.contrib import admin
from .models import Program, Blog, TeamMember

# Register Program model
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'created_at')  # Columns in the admin list view
    list_filter = ('date', 'created_at')           # Filters in the sidebar
    search_fields = ('title', 'description')       # Searchable fields
    ordering = ('-created_at',)                    # Default ordering
    date_hierarchy = 'date'                        # Adds date navigation

# Register Blog model
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'date'

# Register TeamMember model
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')
    search_fields = ('name', 'title', 'bio')
    list_filter = ('title',)
    ordering = ('name',)