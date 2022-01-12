from django.contrib import admin
from Core.models import TextMessage

@admin.register(TextMessage)
class TextMessageAdmin(admin.ModelAdmin):
    list_display = ('id','text','showcase','author')