from django.contrib import admin
from Core.models import Role

class RoleInline(admin.TabularInline):
    model = Role
    extra = 0