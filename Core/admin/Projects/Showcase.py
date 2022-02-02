from django.contrib import admin
from Core.models import Showcase, ShowcaseUpdate

class ShowcaseInline(admin.TabularInline):
    model = Showcase
    extra = 0
    

class ShowcaseUpdateInline(admin.TabularInline):
    model = ShowcaseUpdate
    extra = 0
    
    
@admin.register(Showcase)
class ShowcaseAdmin(admin.ModelAdmin):
    list_display = ('id','name','project','creator')
    inlines = [ShowcaseUpdateInline]