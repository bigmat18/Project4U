from Core.models import Message
from rest_framework import generics, viewsets
from ..serializers import MessageSerializer

class MessageListCreate(generics.ListCreateAPIView,
                        viewsets.GenericViewSet):
    pass