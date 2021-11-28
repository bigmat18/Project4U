from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
import debug_toolbar
from .doc import (schema_view, registration_schema_view, 
                  login_schema_view, logout_schema_view)


admin.site.site_header = 'Project4U Administration'
urlpatterns = [
   path("admin/", admin.site.urls),
   url(r'^doc/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('__debug__/', include(debug_toolbar.urls)),

   # -------- USER REGISTRATION UTILITES ------
   path("api/auth/registration/", registration_schema_view, name="registration"),
   path("api/auth/login/", login_schema_view, name="login"),
   path("api/auth/logout/", logout_schema_view, name="logout"),
   # -------- USER REGISTRATION UTILITES ------

   # -------- API ------
   path('api/', include('Users.urls')),
   # -------- API ------
      
   # -------- WEB-APP ------
   path('', include('Core.urls'))
   # -------- WEB-APP ------
] 