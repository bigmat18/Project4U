from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.conf.urls.static import static
from django.conf import settings

from Core.views import homepageView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="API Project4U",
      default_version='v1',
      description=
      """
      API create per il funzionamento degli applicativi di Project4U, sito web project4u.it (project4u.me, project-4u.it) e l'app Project4U. L'API è ha esclusivo uso di questi applicativi
      è necessario infatti possedere un API-KEY rilasciabile solo per ambienti autorizzati dal nostro team di sviluppo. REST API sviluppata da Giuntoni Matteo in python e django. 
      Link Project4U Admin-Pannel: http://p4u-env.eba-mc4u3jum.us-east-2.elasticbeanstalk.com/
      Link WebSite: http://project4u.it.s3-website.eu-south-1.amazonaws.com/Home
      Link GitHub Sviluppatore: https://github.com/Matteo181202
      Link Github Progetto: https://github.com/Project4UTeam
      """,
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="mat.giu2002@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.IsAdminUser],
)


urlpatterns = [
   path("", homepageView, name="homepage"),
   path("admin/", admin.site.urls),
   url(r'^doc/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

   # -------- USER REGISTRATION UTILITES ------
   path("api-auth/", include("rest_framework.urls")),
   path("api/rest-auth/", include("rest_auth.urls")),
   path("api/rest-auth/registration/", include("rest_auth.registration.urls")),
   # -------- USER REGISTRATION UTILITES ------

   # -------- API ------
   path('api/', include('Users.urls')),
   # -------- API ------
] 

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)