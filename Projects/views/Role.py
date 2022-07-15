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
    
    def is_creator(self, request, view, action) -> bool:
        if action not in ["create", "list"]: 
            role = view.get_object()
            project = view.get_project(role.project.id)        
        else: project = view.get_project()
        return request.user == project.creator
    
    def is_inside_project(self, request, view, action) -> bool:
        project = view.get_project()
        return request.user == project.creator or project.users.filter(id=request.user.id).exists()



class RoleBaseView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, RoleAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)

    def get_project(self, id=None):
        if hasattr(self, "project"): return self.project
        if not id: id = self.kwargs['id']
        self.project = Project.objects.filter(id=id)\
                                      .select_related("creator")\
                                      .prefetch_related("users")\
                                      .first()
        return self.project



class RoleListCreateView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         RoleBaseView):
    """
    list:
    Restituisce la lista dei ruoli.
    
    Restituisce una lista dei ruoli del progetto al quale è stato passato l'id nell'url.
    Solamente colore che fanno parte del progetto possono visualizzare tutti i ruoli.
    
    create:
    Crea un ruolo in un progetto.
    
    Crea un ruolo nel progetto a cui è stato passato l'id. Soltato il creatore del proggetto può
    creare un nuovo ruolo.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    
    def perform_create(self, serializer):
        serializer.save(project=self.get_project())
    
    
    
class RoleUpdateDestroyView(mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            RoleBaseView):
    """
    update:
    Aggiorna una ruolo.

    Aggiorna il dati del ruolo di cui è stato passato l'id nell'url. 
    Soltato il creatore del progetto può aggiornare un ruolo.
    
    partial_update:
    Aggiorna un ruolo.

    Aggiorna il dati del ruolo di cui è stato passato l'id nell'url. 
    Soltato il creatore del progetto può aggiornare un ruolo.
    Vengono restituiti solo i campi modificati.
        
    destroy:
    Elimina una ruolo dal progetto.
    
    Elimina il ruolo dal progetto di cui è stato passato l'id nell'url. 
    Soltato il creatore del progetto può eliminare una ruolo.
    """
    lookup_field = "id"
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    
    def update(self,request,*args, **kwargs):
        response = super().update(request,*args, **kwargs)
        if response.status_code != 200: return response
        return Response(data=request.data,
                        status=response.status_code,
                        headers=response.headers)