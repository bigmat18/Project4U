import imp
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from Users.serializers import (UsersDetailsSerializer, UsersListSerializer,
                               CurrentUserInfoSerializer, CurrentUserImageSerializer)
from Projects.serializers import ProjectListSerializer
from rest_auth.views import UserDetailsView
from Core.models import User, Project

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from django.db.models import Q


                    
class UserRetrieveUpdateView(UserDetailsView,
                             viewsets.GenericViewSet):    
    """
    get:
    Recupera i dati dell'utente loggato.
    
    Recupera i dati dell'utente attualmente loggato, quindi i dati che vengono visti sono quelli di 
    chi ha fatto la richiesa.
    
    put:
    Aggiorna i dati dell'utente loggato.
    
    Aggiorna (PUT, PATCH) i dati dell'utente loggato, cioè di quello che ha fatto la richiesta. 
    E' possibili aggiornare si in modo parziale (PATCH) che totale (PUT). Ritorna solo i dati aggiornati.
    ------ Anche se non mostrato è possibili aggiornare l'immagine profilo ------
    
    patch:
    Aggiorna i dati dell'utente loggato
    
    Aggiorna (PUT, PATCH) i dati dell'utente loggato, cioè di quello che ha fatto la richiesta. 
    E' possibili aggiornare si in modo parziale (PATCH) che totale (PUT). Ritorna solo i dati aggiornati.
    ------ Anche se non mostrato è possibili aggiornare l'immagine profilo ------
    """
    
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        if response.status_code != 200: return response
        if "image" in request.data: request.data['image'] = response.data['image']
        return Response(data=request.data,
                        status=response.status_code,
                        headers=response.headers)
    
    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        if response.status_code != 200: return response
        if "image" in request.data: request.data['image'] = response.data['image']
        return Response(data=request.data,
                        status=response.status_code,
                        headers=response.headers)



class UsersListView(generics.ListAPIView,
                   viewsets.GenericViewSet):

    """
    list:
    Ritorna la lista di tutti gli utente.

    Ritorna una lista di tutti gli utente salvati nel DB in un formato ridotto. E' necessario
    essere autenticati per ricere una risposta. Questo endpotins servità quando ci sarà
    la sezione dedica alla ricerca di persone da aggiungere a progetti.
    """
    serializer_class = UsersListSerializer
    queryset = User.objects.filter(active=True)



class UsersRetriveView(generics.RetrieveAPIView,
                      viewsets.GenericViewSet):
    """
    retrieve:
    Ristituisce i dettagli di un'utente.

    Ritorna tutti i dettagli di un utente di cui è stato passato la secret_key nell'url.
    Serve quando si entra per esempio nel profilo di un'utente
    """
    serializer_class = UsersDetailsSerializer
    queryset = User.objects.filter(active=True)
    lookup_field = "secret_key"
    
    
    
class UserProjectsListView(generics.ListAPIView,
                           viewsets.GenericViewSet):
    """
    list:
    Vedi la lista dei progetti dell'utente loggato.
    
    Vedi la lista dei progetti dell'utente loggato (cioè di quello che fa la richiesta), i progetti
    che vede sono quelli o che ha creato o che è dentro come partecipante.
    """
    serializer_class = ProjectListSerializer
    queryset = Project.objects.all()
    
    def get_queryset(self):
        return Project.objects.filter(Q(creator=self.request.user.id) | 
                                      Q(users=self.request.user.id))
    


@method_decorator(name="get",decorator=swagger_auto_schema(
                             responses={"200":openapi.Schema(type=openapi.TYPE_OBJECT,
                                                            properties={"image":openapi.Schema(
                                                                        type=openapi.TYPE_STRING)})}))
class UserImageView(APIView):

    def get(self, request, *args, **kwargs):
        """
        Restituisce l'immage dell'utente loggato.
        
        Restituisce solo l'immage dell'utente loggato (cioè di quello che ha fatto la richesta).
        Endpoints da utilizzare per l'ateprima dell'immage dell'utente per esempio in una navbar.
        """
        user = User.objects.get(id=request.user.id)
        serializer = CurrentUserImageSerializer(user)
        return Response(status=status.HTTP_200_OK,data=serializer.data)


@method_decorator(name="get",decorator=swagger_auto_schema(
                             responses={"200":CurrentUserImageSerializer}))
class UserInfoView(APIView):
    
    def get(self, request, *args, **kwargs):
        """
        Restituisce dati utente loggato.
        
        Restituisce dati dell'utente loggato (cioè di quello che ha fatto la richesta) in un formato ridotto.
        Questo endpoints serve per inserire i dati in picoli paragrafi come la navbar del sito o un'ateprima dell'account
        quando l'utente naviga per l'app.
        """
        user = get_object_or_404(User, id=request.user.id)
        serializer = CurrentUserInfoSerializer(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)