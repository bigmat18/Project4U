from django.contrib import admin
from Core.models import Showcase

class ShowcaseInline(admin.TabularInline):
    model = Showcase
    extra = 0