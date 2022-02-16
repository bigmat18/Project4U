from django.contrib import admin
from Core.models import Poll, PollOption

class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 0


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id','text','showcase','author')
    inlines = [PollOptionInline]
