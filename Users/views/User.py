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
    Recupera i dati dell'utente loggato
    
    Recupera i dati dell'utente loggato
    
    put:
    Aggiorna i dati dell'utente loggato
    
    Aggiorna (PUT, PATCH) i dati dell'utente loggato. E' possibili aggiornare si in modo parziale (PATCH) che totale (PUT).
    Ritorna solo i dati aggiornati.
    ------ Anche se non mostrato è possibili aggiornare l'immagine profilo ------
    
    patch:
    Aggiorna i dati dell'utente loggato
    
    Aggiorna (PUT, PATCH) i dati dell'utente loggato. E' possibili aggiornare si in modo parziale (PATCH) che totale (PUT).
    Ritorna solo i dati aggiornati.
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
    Ritorna la lista degli utenti.

    Ritorna una lista di utenti in un formato ridetto. E' necessario
    essere autenticati per ricere una risposta.
    """
    serializer_class = UsersListSerializer
    queryset = User.objects.filter(active=True)



class UsersRetriveView(generics.RetrieveAPIView,
                      viewsets.GenericViewSet):
    """
    retrieve:
    Ristituisce i dettagli di un'utente.

    Ritorna tutti i dettagli di un utente di cui è stato passato lo secret_key nell'url.
    """
    serializer_class = UsersDetailsSerializer
    queryset = User.objects.filter(active=True)
    lookup_field = "secret_key"
    
    
    
class UserProjectsListView(generics.ListAPIView,
                           viewsets.GenericViewSet):
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
        Restituisce l'immage dell'utente loggato
        
        Restituisce l'immage dell'utente loggato
        """
        user = User.objects.get(id=request.user.id)
        serializer = CurrentUserImageSerializer(user)
        return Response(status=status.HTTP_200_OK,data=serializer.data)




class UserInfoView(APIView):
    
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        serializer = CurrentUserInfoSerializer(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)