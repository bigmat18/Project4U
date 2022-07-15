from django.contrib import admin
from Core.models import ProjectQuestion, ProjectAnswer


class ProjectAnswerInline(admin.TabularInline):
    model = ProjectAnswer
    extra = 0


@admin.register(ProjectQuestion)
class ProjectQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'created_at', 'updated_at', 'question', 'author')
    inlines = [ProjectAnswerInline]