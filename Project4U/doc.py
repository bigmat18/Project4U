from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
      Link Website: http://project4u.it
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


#--------------- REGISTRATION DOC ------------
registration_201 = \
    openapi.Response(description="Registrazione avvenuta con successo",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={"key":openapi.Schema(title="auth-token",
                                                        type=openapi.TYPE_STRING)}))
    
    
registration_400_1 = \
    openapi.Response(description="Nel caso venga ommesso un campo",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={"Nome del campo":openapi.Schema(
                            description="Questo campo non può essere omesso",
                            type=openapi.TYPE_STRING)}))
    
    
registration_400_2 = \
    openapi.Response(description="Caso in cui un utente con la stessa mail sia registrato",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={"email":openapi.Schema(
                            description="Un altro utente si è già registrato con questo indirizzo e-mail.",
                            type=openapi.TYPE_STRING)}))
    
    
registration_400_3 = \
    openapi.Response(description="Se le due password non sono uguali",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={"non_field_errors":openapi.Schema(
                            description="The two password fields didn't match.",
                            type=openapi.TYPE_STRING)}))
    
    
registration_400_4 = \
    openapi.Response(description="Se la password non rispetta il formato richiesto",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={"password1":openapi.Schema(
                            description="Una lista con tutti i messaggi di errori che la password ha generato",
                            type=openapi.TYPE_STRING)}))
    
registration_schema_view = \
   swagger_auto_schema(method='post',
                       operation_description="Registrazione utente con email, password (password1 e password2), first_name, last_name, date_birth, location (opzionale)",
                       operation_summary="Registrazione nuovo utente",
                       responses={"201":registration_201,
                                 "1: 400":registration_400_1,
                                 "2: 400":registration_400_2,
                                 "3: 400":registration_400_3,
                                 "4: 400":registration_400_4})\
                                     (RegisterView.as_view())
#--------------- REGISTRATION DOC ------------




#--------------- LOGIN DOC ------------
login_200 = \
    openapi.Response(
        description="Login avvenuto con successo",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"key":openapi.Schema(
                title="auth-token",
                type=openapi.TYPE_STRING)}))
    
    
login_400 = \
    openapi.Response(
        description="Credenziali sbagliate",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"non_field_errors":openapi.Schema(
                description="Impossibile eseguire il login con le credenziali immesse.",
                type=openapi.TYPE_STRING)}))


login_schema_view = \
   swagger_auto_schema(method='post',
                       operation_description="Login utente con email e password",
                       operation_summary="Login utente registrato",
                       responses={"200":login_200,
                                "400":login_400})\
                                    (LoginView.as_view())
#--------------- LOGIN DOC ------------



#--------------- USER-DETAIL DOC ------------
logout_schema_view = \
   swagger_auto_schema(methods=["get","post"],
                       operation_description="""
                                            Slogga un utente loggato nel sistema rimuovendo il token a lui associato. E' possibili chiamare questo endpoints
                                            sia come richiesta POST che GET.
                                             """,
                       operation_summary="Slogga un utente loggato nel sistema")(LogoutView.as_view())
#--------------- USER-DETAIL DOC ------------