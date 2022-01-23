from django.contrib import admin
from Core.models import ProjectTag

@admin.register(ProjectTag)
class ProjectTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
