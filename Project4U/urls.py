from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from Users.views import EmailCreateView
from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView, LogoutView

schema_view = get_schema_view(
   openapi.Info(
      title="API Project4U",
      default_version='v1',
      description=
      """
      API create per il funzionamento degli applicativi di Project4U, sito web project4u.it e l'app Project4U. L'API è ha esclusivo uso degli sviluppatori di Project4U,
      è necessario infatti possedere un API-KEY rilasciata solo per ambienti autorizzati dal nostro team amministrativo. REST API sviluppata da Giuntoni Matteo in python e django. 
      Link Project4U Admin-Pannel: http://admin.project4u.it
      Link website: http://project4u.it
      Link GitHub sviluppatore: https://github.com/Matteo181202
      Link Github progetto: https://github.com/Project4UTeam
      """,
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="teamproject4u@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.IsAdminUser],
)


urlpatterns = [
   path("admin/", admin.site.urls),
   url(r'^doc/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

   # -------- USER REGISTRATION UTILITES ------
   path("api/auth/login/", LoginView.as_view(), name="login"),
   path("api/auth/logout/", LogoutView.as_view(), name="logout"),
   path("api/auth/registration/", RegisterView.as_view(), name="registration"),
   # -------- USER REGISTRATION UTILITES ------

   # -------- API ------
   path('api/profile/', include('Users.urls')),
   # -------- API ------
   
   path('api/email/', EmailCreateView.as_view(), name="email-create"),
   
   # -------- WEB-APP ------
   path('', include('Core.urls'))
   # -------- WEB-APP ------
] 