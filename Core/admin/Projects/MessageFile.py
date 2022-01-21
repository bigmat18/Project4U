from django.contrib import admin
from Core.models import MessageFile

class MessageFileInline(admin.TabularInline):
    model = MessageFile
    extra = 0