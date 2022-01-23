from django.contrib import admin
from Core.models import TextMessage
from Core.admin import MessageFileInline

@admin.register(TextMessage)
class TextMessageAdmin(admin.ModelAdmin):
    list_display = ('id','text','showcase','author')
    inlines = [MessageFileInline]