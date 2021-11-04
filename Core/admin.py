from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from Core.models import *
from django.contrib.sites.models import Site
from Core.models import Email
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

from import_export import resources
from import_export.admin import ImportExportModelAdmin

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
    

# ------------ ADMIN IMPORT-EXPORT ---------
class EmailResource(resources.ModelResource):
    class Meta:
        model = Email
        exclude = ('id','added_at',)
        import_id_fields = ('email', 'first_name', 'last_name',)

class EmailImportExport(ImportExportModelAdmin):
    resource_class = EmailResource
# ------------ ADMIN IMPORT-EXPORT ---------


admin.site.register(Email, EmailImportExport)

admin.site.unregister(Group)

admin.site.unregister(Site)

admin.site.unregister(EmailAddress)

admin.site.unregister(SocialAccount)

admin.site.unregister(SocialApp)

admin.site.unregister(SocialToken)
