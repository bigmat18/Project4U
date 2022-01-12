from ..serializers import ShowcaseSerializer
from rest_framework import generics, viewsets
from Core.models import Showcase, Project, Message

class ShowcaseListCreateView(generics.ListCreateAPIView,
                             viewsets.GenericViewSet):
    """
    list:
    Visualizza la lista delle bacheche.
    
    Visualizza una lista di tutte le bacheche del progetto di cui è stato passato l'id.
    
    create:
    Crea una nuova bacheca.
    
    Crea una nuova bacheca nel progetto di cui è stato passato l'id.
    """
    serializer_class = ShowcaseSerializer
    queryset = Showcase.objects.all()
    
    def get_project(self):
        project_id = self.kwargs['id']
        return generics.get_object_or_404(Project, id=project_id)
    
    def get_queryset(self):
        return Showcase.objects.filter(project__id=self.kwargs['id'])
    
    def perform_create(self, serializer):
        instance = serializer.save(project=self.get_project())
        instance.users.add(self.request.user)