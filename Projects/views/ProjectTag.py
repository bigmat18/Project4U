from ..serializers import ProjectTagSerializer
from Core.models import ProjectTag
from rest_framework import generics, viewsets


class ProjectTagListCreateView(generics.ListCreateAPIView,
                               viewsets.GenericViewSet):
    """
    list:
    Lista di tutti i tags progetti.
    
    Vedi una lista di tutti i tags progetti esistenti
    
    create:
    Crea tags progetto.
    
    Crea un nuovo tags progetto.
    """
    serializer_class = ProjectTagSerializer
    queryset = ProjectTag.objects.all()
