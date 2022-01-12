from Core.models import Message, Showcase
from rest_framework import generics, mixins, viewsets
from ..serializers import MessageSerializer
from rest_framework.response import Response

class MessageListView(generics.ListAPIView,
                      viewsets.GenericViewSet):
    serializer_class = MessageSerializer
    
    def get_showcase(self):
        showcase_id = self.kwargs['id']
        return generics.get_object_or_404(Showcase, id=showcase_id)
    
    def get_queryset(self):
        return Message.objects.filter(showcase=self.get_showcase())\
                              .select_related('text_message', 'event')
