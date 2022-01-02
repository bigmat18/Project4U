from django.http import response
from rest_framework import generics, mixins
from rest_framework import viewsets
from rest_framework.response import Response

from Core.models.Projects.Project import Project
from ..serializers import RoleSerializer
from Core.models import Role
from rest_access_policy import AccessPolicy
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings


class RoleAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_inside_project"
        },
        {
            "action": ["destroy", "update", "partial_update", "create"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_creator"
        },
    ]
    
    def get_project(self,view):
        project_id = view.kwargs['id']
        project = generics.get_object_or_404(Project, id=project_id)
        return project
    
    def is_creator(self, request, view, action) -> bool:
        if action != "create": 
            role = view.get_object()
            project = generics.get_object_or_404(Project, id=role.project.id)
        else: project = self.get_project(view)
        return request.user == project.creator
    
    def is_inside_project(self, request, view, action) -> bool:
        project = self.get_project(view)
        return request.user == project.creator or project.users.filter(id=request.user.id).exists()



class RoleListCreateView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """
    list:
    Restituisce la lista di ruolo.
    
    Restituisce una lista di ruolo per il progetto al quale è stato passato l'id.
    Solamente colore che fanno parte del progetto possono visualizzare tutti i ruoli.
    
    create:
    Crea un ruolo.
    
    Crea un ruolo nel progetto a cui è stato passato l'id. Soltato il creatore del proggetto può
    creare un nuovo ruolo.
    """
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, RoleAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)

    
    def perform_create(self, serializer):
        id = self.kwargs['id']
        project = generics.get_object_or_404(Project, id=id)
        serializer.save(project=project)
    
    
    
class RoleUpdateDestroyView(mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """
    update:
    Aggiorna una regola.

    Aggiorna il dati di una regola. Soltato il creatore del progetto può aggiornare una regola.
    
    partial_update:
    Aggiorna una regola.

    Aggiorna il dati di una regola. Soltato il creatore del progetto può aggiornare una regola.
    Vengono restituiti solo i campi modificati.
        
    destroy:
    Elimina una regola.
    
    Elimina una regola dal progetto. Soltato il creatore del progetto può eliminare una regola.
    """
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, RoleAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    
    def update(self,request,*args, **kwargs):
        response = super().update(request,*args, **kwargs)
        if response.status_code != 200: return response
        return Response(data=request.data,
                        status=response.status_code,
                        headers=response.headers)