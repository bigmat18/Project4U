from django.contrib import admin
from Core.models import Project
from Core.admin import RoleInline, UserProjectInline, ShowcaseInline
from import_export.admin import ImportExportMixin
from import_export import resources


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project


@admin.register(Project)
class ProjectAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'creator')
    resource_class = ProjectResource
    inlines = [RoleInline, UserProjectInline, ShowcaseInline]

    