from django.contrib import admin
from Core.models import ExternalProject

class ExternalProjectInline(admin.TabularInline):
    model = ExternalProject
    extra = 0