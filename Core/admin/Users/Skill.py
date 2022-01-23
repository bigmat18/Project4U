from django.contrib import admin
from Core.models import Skill, UserSkill
from import_export.admin import ImportExportMixin
from import_export import resources


class SkillResource(resources.ModelResource):
    class Meta:
        model = Skill


class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 0


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin, ImportExportMixin):
    list_display = ('id', 'name', 'type_skill')
    inlines = [UserSkillInline]
    resource_class = SkillResource
