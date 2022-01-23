from rest_framework import generics, mixins
from rest_framework import viewsets
from Core.models import Project, Showcase
from rest_framework.response import Response
from Projects.serializers.Project import ProjectDetailSerializer
from ..serializers import ProjectListSerializer
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated
from rest_access_policy.access_policy import AccessPolicy
from django.conf import settings



class ProjectsAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["destroy", "update", "partial_update"],
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




class ProjectsListCreateView(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
    Mostra una lista di progetti.
    
    Motra una lista di tutti i progetti salvati. 
    
    create:
    Aggiungi un progetto.
    
    Aggiungi un nuovo progetto con te come creatore.
    """
    serializer_class = ProjectListSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, ProjectsAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)

    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)



class ProjectsRUDView(generics.RetrieveUpdateDestroyAPIView,
                      viewsets.GenericViewSet):
    """
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
    
    partial_update:
    Aggiorna il progetto
    
    Dato un id di un progetto puoi agiornare 1 o più suoi dati. E' possibile esseguire l'aggiornamento
    soltato se si è il creatore del progetto. Vengono restituiti soltato i campi modificati.
    """
    serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, ProjectsAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    
    def update(self,request,*args, **kwargs):
        response = super().update(request,*args, **kwargs)
        if response.status_code != 200: return response
        if "image" in request.data: request.data['image'] = response.data['image']
        return Response(data=request.data,
                        status=response.status_code,
                        headers=response.headers)
