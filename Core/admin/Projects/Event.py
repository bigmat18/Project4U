from django.contrib import admin
from Core.models import Event, EventTask, EventUpdate
from Core.admin import MessageFileInline

class EventTaskInline(admin.TabularInline):
    model = EventTask
    extra = 0
    
    
class EventUpdateInline(admin.TabularInline):
    model = EventUpdate
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','text','showcase','author')
    inlines = [EventUpdateInline, EventTaskInline, MessageFileInline]
