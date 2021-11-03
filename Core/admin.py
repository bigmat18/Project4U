from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from Core.models import (User, Skill, UserSkill, SearchCard, Tag,
                         Project, UserProject, Role)

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


admin.site.register(Skill)

admin.site.register(UserSkill)


admin.site.register(SearchCard)

admin.site.register(Project)

admin.site.register(Tag)

admin.site.register(UserProject)

admin.site.register(Role)


admin.site.unregister(Group)
