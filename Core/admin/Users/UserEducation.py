from django.contrib import admin
from Core.models import UserEducation

class UserEducationInline(admin.TabularInline):
    model = UserEducation
    extra = 0