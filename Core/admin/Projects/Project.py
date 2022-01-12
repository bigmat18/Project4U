from django.contrib import admin
from Core.models import Project
from Core.admin import RoleInline, UserProjectInline, ShowcaseInline

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'creator')
    inlines = [RoleInline, UserProjectInline, ShowcaseInline]
