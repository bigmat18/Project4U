from django.contrib import admin
from Core.models import TextPost


@admin.register(TextPost)
class TextPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'created_at', 'updated_at', 'text', 'author')