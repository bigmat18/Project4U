from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from ..serializers import TextMessageSerializer
from Core.models import Showcase

class TextMessageCreateView(generics.CreateAPIView,
                            viewsets.GenericViewSet):
    serializer_class = TextMessageSerializer
    
    def get_showcases(self):
        return get_object_or_404(Showcase, id=self.kwargs['id'])
    
    def perform_create(self, serializer):
        serializer.save(showcase=self.get_showcases(),
                        type_message="TEXT",
                        author=self.request.user)