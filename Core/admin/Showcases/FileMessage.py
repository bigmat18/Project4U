from django.contrib import admin
from Core.models import FileMessage

class FileMessageInline(admin.TabularInline):
    model = FileMessage
    extra = 0