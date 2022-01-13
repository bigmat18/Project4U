from ..serializers import ShowcaseSerializer
from rest_framework import generics, viewsets
from Core.models import Showcase, Project, Message
from rest_access_policy import AccessPolicy
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings


class ShowcaseAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list","create"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_inside_project"
        }
    ]
    
    def is_inside_project(self, request, view, action) -> bool:
        project = generics.get_object_or_404(Project, id=view.kwargs['id'])
        return (request.user == project.creator or 
                project.users.filter(id=request.user.id).exists())



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
    permission_classes = [IsAuthenticated, ShowcaseAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_project(self):
        project_id = self.kwargs['id']
        return generics.get_object_or_404(Project, id=project_id)
    
    def get_queryset(self):
        return Showcase.objects.filter(project__id=self.kwargs['id'])
    
    def perform_create(self, serializer):
        instance = serializer.save(project=self.get_project())
        instance.users.add(self.request.user)