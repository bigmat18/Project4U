from django.contrib import admin
from Core.models import Project, Role, UserProject, Showcase
from import_export.admin import ImportExportMixin
from import_export import resources


class RoleInline(admin.TabularInline):
    model = Role
    extra = 0
    
    
class UserProjectInline(admin.TabularInline):
    model = UserProject
    extra = 0
    
    
class ShowcaseInline(admin.TabularInline):
    model = Showcase
    extra = 0
    

# ------------ ADMIN IMPORT-EXPORT ---------
class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
# ------------ ADMIN IMPORT-EXPORT ---------


@admin.register(Project)
class ProjectAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at', 'creator')
    resource_class = ProjectResource
    inlines = [RoleInline, UserProjectInline, ShowcaseInline]

    