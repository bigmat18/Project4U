from django.contrib import admin
from Core.models import Skill, UserSkill

class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 0

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type_skill')
    inlines = [UserSkillInline]