from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin
from rest_framework_api_key.models import APIKey
from import_export import resources
from import_export.admin import ImportExportMixin


# ------------ ADMIN IMPORT-EXPORT ---------
class ApiKeyResource(resources.ModelResource):
    class Meta:
        model = APIKey

class ApiKeyImportExport(ImportExportMixin, APIKeyModelAdmin):
    resource_class = ApiKeyResource
# ------------ ADMIN IMPORT-EXPORT ---------


admin.site.unregister(APIKey)
admin.site.register(APIKey, ApiKeyImportExport)