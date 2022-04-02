from rest_framework import viewsets, generics
from ..serializers import TextPostSerializer
from Core.models import TextPost
    
    
class TextPostCreateView(generics.CreateAPIView,
                         viewsets.GenericViewSet):
    pass


class TextPostUpdateDestroyView(generics.UpdateAPIView,
                                generics.DestroyAPIView,
                                viewsets.GenericViewSet):
    pass