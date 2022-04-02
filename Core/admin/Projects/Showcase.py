from django.contrib import admin
from Core.models import Showcase, ShowcaseUpdate


class ShowcaseUpdateInline(admin.TabularInline):
    model = ShowcaseUpdate
    extra = 0
    
    
@admin.register(Showcase)
class ShowcaseAdmin(admin.ModelAdmin):
    list_display = ('id','name','project','creator')
    inlines = [ShowcaseUpdateInline]