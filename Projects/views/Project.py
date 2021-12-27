from rest_framework.viewsets import ModelViewSet
from Core.models import Project
from ..serializers import ProjectSerializer
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated
from rest_access_policy.access_policy import AccessPolicy
from django.conf import settings



class ProjectsAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["destroy", "update"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_creator"
        },
        {
            "action": ["list", "create", "retrieve"],
            "principal": "*",
            "effect": "allow"
        }
    ]
    
    def is_creator(self, request, view, action) -> bool:
        project = view.get_object()
        return request.user == project.creator




class ProjectsViewSet(ModelViewSet):
    """
    list:
    Mostra una lista di progetti.
    
    Motra una lista di tutti i progetti salvati. 
    
    create:
    Aggiungi un progetto.
    
    Aggiungi un nuovo progetto con te come creatore.
    
    retrieve:
    Mostra un progetto
    
    Dato un id di un progetto mostra tutti i dati di quel progetto.
    
    destroy:
    Elimina un progetto.
    
    Dato un id di un progetto è possibili eliminarlo soltato in caso si sia il creatore.
    
    update:
    Aggiorna il progetto
    
    Dato un id di un progetto puoi agiornare 1 o più suoi dati. E' possibile esseguire l'aggiornamento
    soltato se si è il creatore del progetto.
    """
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, ProjectsAccessPolicy]
    #if not settings.DEBUG: permission_classes.append(HasAPIKey)

    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
