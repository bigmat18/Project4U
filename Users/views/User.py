from rest_framework import generics, viewsets
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from Users.serializers import UserDetailSerializer, UserListSerializer
from Core.models import User


class UserListView(generics.ListAPIView,
                viewsets.GenericViewSet):

    """
    list:
    Ritorna la lista degli utenti.

    Ritorna una lista di utenti in un formato ridetto. E' necessario
    essere autenticati per ricere una risposta.
    """
    serializer_class    = UserListSerializer
    queryset            = User.objects.filter(active=True)
    permission_classes  = [IsAuthenticated]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)



class UserRetriveView(generics.RetrieveAPIView,
                        viewsets.GenericViewSet):
    """
    retrieve:
    Ristituisce i dettagli di un'utente.

    Ritorna tutti i dettagli di un utente di cui è stato passato lo slug nell'ulr
    """
    serializer_class    = UserDetailSerializer
    queryset            = User.objects.filter(active=True)
    lookup_field        = "slug"
    permission_classes  = [IsAuthenticated]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)