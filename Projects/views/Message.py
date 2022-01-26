from Core.models import Message, Showcase
from rest_framework import generics, viewsets
from ..serializers import MessageSerializer, TextMessageSerializer
import django_filters as filters
from rest_access_policy import AccessPolicy
from django.shortcuts import get_object_or_404


from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class MessagePagintation(PageNumberPagination):
    page_size = 25


class MessageAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "create"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_inside_showcase"
        },
    ]
    
    def is_inside_showcase(self, request, view, action) -> bool:
        showcase = generics.get_object_or_404(Showcase, id=view.kwargs['id'])
        return (request.user == showcase.creator or 
                showcase.users.filter(id=request.user.id).exists())


class MessageFilter(filters.FilterSet):
    
    class Meta:
        model = Message
        fields = ["type_message"]
    

class MessageListView(generics.ListAPIView,
                      viewsets.GenericViewSet):
    """
    list:
    Restituisce la lista dei messaggi.
    
    Restituisce una lista con tutti i messaggi della bacheca di cui è stato passato l'id.
    E' possibile filtrare i tipi di messaggi scrivendo nell'url '?type_message=' ed accanto il tipo di messaggio
    fra TEXT, IDEA, EVENT.
    Soltato i partecipanti alla bacheca possono vedere la lista dei messaggi.
    
    -----IMPORTANTE----
    Il campo 'content' non è una stringa ma restituisce un oggetto con i capi del messaggio, vedi in fondo
    alla pagina TextMessage e Event modelli per vedere i campi.
    """
    serializer_class = MessageSerializer
    filterset_class = MessageFilter
    pagination_class = MessagePagintation
    permission_classes = [IsAuthenticated, MessageAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)

    
    def get_showcase(self):
        showcase_id = self.kwargs['id']
        return generics.get_object_or_404(Showcase, id=showcase_id)
    
    def get_queryset(self):
        return Message.objects.filter(showcase=self.get_showcase())\
                              .select_related('text_message', 'event')




class TextMessageCreateView(generics.CreateAPIView,
                            viewsets.GenericViewSet):
    """
    create:
    Create un messaggio testuale
    
    Crea un nuovo messaggio testuale nella bacheca di cui è stato passato l'id.
    Soltato i partecipanti alla bacheca possono creare un messaggio.
    """
    serializer_class = TextMessageSerializer
    permission_classes = [IsAuthenticated, MessageAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_showcases(self):
        return get_object_or_404(Showcase, id=self.kwargs['id'])
    
    def perform_create(self, serializer):
        serializer.save(showcase=self.get_showcases(),
                        type_message="TEXT",
                        author=self.request.user)