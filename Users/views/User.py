from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from Users.serializers import UserDetailSerializer, UserListSerializer
from Core.models import User

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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
    
    
class UserImageView(APIView):
    
    @swagger_auto_schema(responses={"200":
        openapi.Schema(type=openapi.TYPE_OBJECT,
                       properties={"image":openapi.Schema(
                           type=openapi.TYPE_STRING)})})
    def get(self,request):
        """
        Restituisce l'immage dell'utente loggato
        
        Restituisce l'immage dell'utente loggato
        """
        user = User.objects.get(id=request.user.id)
        if user.image: return Response(status=status.HTTP_200_OK,data={"image":user.image})
        else: return Response(status=status.HTTP_200_OK,data={"image":None})