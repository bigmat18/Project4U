from django.contrib import admin
from Core.models import Event, EventTask


class EventTaskInline(admin.TabularInline):
    model = EventTask
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','name','showcase','author')
    inlines = [EventTaskInline]
