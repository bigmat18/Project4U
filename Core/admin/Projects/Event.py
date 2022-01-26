from django.contrib import admin
from Core.models import Event, EventTask
from Core.admin import MessageFileInline

class EventTaskInline(admin.TabularInline):
    model = EventTask
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','description','showcase','author')
    inlines = [EventTaskInline, MessageFileInline]
