from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Core.models import User, ExternalProject, UserEducation
from Core.admin import UserSkillInline


class UserEducationInline(admin.TabularInline):
    model = UserEducation
    extra = 0


class ExternalProjectInline(admin.TabularInline):
    model = ExternalProject
    extra = 0


@admin.register(User)
class User(UserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name','blocked', 'date_joined')
    inlines = [UserSkillInline, UserEducationInline, ExternalProjectInline]
    list_filter = ('blocked', 'active')
    fieldsets = (('Dati di accesso', {'fields': ('email', 'password','first_name','last_name',)}),
                ('Dati personali', {'fields': ('last_login', 'date_joined', 'image',
                                                'main_role', 'description', 'location')}),
                ('Interazioni', {'fields': ('user_saved', 'project_saved')}),
                ('Stato', {'fields': ('blocked', 'active','admin', 'type_user', 'type_vip')}))  
    
    add_fieldsets = ((None, {
                    'classes': ('wide'),
                    'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}),)

    search_fields       = ['email', 'first_name', 'last_name']
    ordering            = ('-date_joined',)
    filter_horizontal   = ()
