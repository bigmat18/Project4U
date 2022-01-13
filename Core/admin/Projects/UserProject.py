from django.contrib import admin
from Core.models import UserProject
from Core.models.Users.User import User

class UserProjectInline(admin.TabularInline):
    model = UserProject
    extra = 0