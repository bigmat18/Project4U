from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from Core.models import UserProject, Project
from ..serializers import UserProjectUpdateSerializer, UserProjectListSerializer
from django.db import IntegrityError
from rest_framework import status
from rest_access_policy import AccessPolicy
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserProjectAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list"],
            "principal": "*",
            "effect": "allow",
        },
        {
            "action": ["create", "update", "partial_update", "destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_creator"
        }
    ]

    def get_project(self, view):
        project_id = view.kwargs['id']
        project = generics.get_object_or_404(Project, id=project_id)
        return project

    def is_creator(self, request, view, action) -> bool:
        if action != "create": 
            user = view.get_object()
            project = generics.get_object_or_404(Project, id=user.project.id)
        else: project = self.get_project(view)
        return request.user == project.creator



@method_decorator(name="create", decorator=swagger_auto_schema(
    responses={"201":UserProjectListSerializer,
               "400":openapi.Schema(type=openapi.TYPE_OBJECT,
                                    properties={"Error":openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Utente già aggiunto al progetto")})}))
class UserProjectListCreateView(generics.ListCreateAPIView,
                                viewsets.GenericViewSet):
    """
    list:
    Vedi la lista degli utenti in un progetto.
    
    Vedi tutti gli utenti dentro il progetto del quale abbiamo passato l'id.
    Endpoints da usare per esempio in un ipotetico form di creazione dei una bacheca per
    vedere la lista degli utenti nel progetto, oppure semplicemente nelle impostazioni del progetto.
    
    create:
    Aggiungi un utente al progetto.
    
    Aggiungi un utente al il proggetto del quale abbiamo passato l'id. 
    Soltato il creatore del progetto può aggiungere utenti.
    """
    serializer_class = UserProjectListSerializer
    queryset = UserProject.objects.all()
    permission_classes = [IsAuthenticated,UserProjectAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_queryset(self):
        project_id = self.kwargs['id']
        return UserProject.objects.filter(project=project_id)\
                                  .order_by("-updated_at")
    
    def perform_create(self, serializer):
        project_id = self.kwargs['id']
        project = get_object_or_404(Project, id=project_id)
        try: serializer.save(project=project)
        except IntegrityError:
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST, 
                                  detail={"Error":"Utente già aggiunto al progetto"})



class UserProjectUpdateDestroyView(generics.UpdateAPIView,
                                   generics.DestroyAPIView,
                                   viewsets.GenericViewSet):
    """
    update:
    Aggiorna i ruoli di un utente.
    
    Aggiorna i ruoli dell'utente del cui è stato passato l'id. 
    Solato il creatore del progetto può eseguire questa operazione.
    
    partial_update:
    Aggiorna i ruoli di un utente.
    
    Aggiorna i ruoli dell'utente del cui è stato passato l'id. 
    Solato il creatore del progetto può eseguire questa operazione.
    
    destroy:
    Rimuove un utente da un progetto.
    
    Rimuove un utente dal progetto del cui è stato passato l'id.
    Solato il creatore del progetto può eseguire questa operazione.
    """
    serializer_class = UserProjectUpdateSerializer
    queryset = UserProject.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated,UserProjectAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)