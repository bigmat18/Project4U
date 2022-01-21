from Core.models import Message, Showcase
from rest_framework import generics, mixins, viewsets
from ..serializers import MessageSerializer
import django_filters as filters
from rest_framework.response import Response



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
    
    -----IMPORTANTE----
    Il campo 'content' non è una stringa ma restituisce un oggetto con i capi del messaggio, vedi in fondo
    alla pagina TextMessage e Event modelli per vedere i campi.
    """
    serializer_class = MessageSerializer
    filterset_class = MessageFilter

    
    def get_showcase(self):
        showcase_id = self.kwargs['id']
        return generics.get_object_or_404(Showcase, id=showcase_id)
    
    def get_queryset(self):
        return Message.objects.filter(showcase=self.get_showcase())\
                              .select_related('text_message', 'event')