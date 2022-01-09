from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from Users.serializers import (UserDetailSerializer, UserListSerializer,
                               CurrentUserImageSerializer)
from rest_auth.views import UserDetailsView
from Core.models import User

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator


                    
class CustomUserDetailsView(UserDetailsView,
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



class UserListView(generics.ListAPIView,
                viewsets.GenericViewSet):

    """
    list:
    Ritorna la lista degli utenti.

    Ritorna una lista di utenti in un formato ridetto. E' necessario
    essere autenticati per ricere una risposta.
    """
    serializer_class = UserListSerializer
    queryset = User.objects.filter(active=True)



class UserRetriveView(generics.RetrieveAPIView,
                      viewsets.GenericViewSet):
    """
    retrieve:
    Ristituisce i dettagli di un'utente.

    Ritorna tutti i dettagli di un utente di cui è stato passato lo slug nell'ulr
    """
    serializer_class = UserDetailSerializer
    queryset = User.objects.filter(active=True)
    lookup_field = "slug"
    
    
    
@method_decorator(name="get",decorator=swagger_auto_schema(
                             responses={"200":openapi.Schema(type=openapi.TYPE_OBJECT,
                                                            properties={"image":openapi.Schema(
                                                                        type=openapi.TYPE_STRING)})}))
class UserImageView(APIView):

    def get(self,request):
        """
        Restituisce l'immage dell'utente loggato
        
        Restituisce l'immage dell'utente loggato
        """
        user = User.objects.get(id=request.user.id)
        serializer = CurrentUserImageSerializer(user)
        return Response(status=status.HTTP_200_OK,data=serializer.data)
