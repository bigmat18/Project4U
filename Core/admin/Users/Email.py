from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from Core.models import Email

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