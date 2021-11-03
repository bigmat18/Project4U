from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from Core.models import *

@admin.register(User)
class User(UserAdmin):
    list_display    = ('id', 'email', 'first_name', 'last_name',
                        'blocked', 'date_joined')
    list_filter     = ('blocked', 'active')
    fieldsets       = (('Dati di accesso', {'fields': ('email', 'password',)}),
                        ('Dati personali', {'fields': ('first_name', 'last_name', 
                                            'last_login', 'date_joined', 'image')}),
                        ('Stato', {'fields': ('blocked', 'active')}),)  
    add_fieldsets   = ((None, {
                        'classes': ('wide'),
                        'fields': ('email', 'first_name', 'last_name', 
                                            'password1', 'password2'),
                        }),)

    search_fields       = ['email', 'first_name', 'last_name']
    ordering            = ('-date_joined',)
    filter_horizontal   = ()

admin.site.unregister(Group)
