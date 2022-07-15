from django.contrib import admin
from Core.models import TextMessage, MessageFile


class MessageFileInline(admin.TabularInline):
    model = MessageFile
    extra = 0

@admin.register(TextMessage)
class TextMessageAdmin(admin.ModelAdmin):
    list_display = ('id','text','showcase','author')
    inlines = [MessageFileInline]
    
    