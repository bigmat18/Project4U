from ..serializers import ShowcaseReadSerializer, ShowcaseWriteSerializer
from rest_framework import generics, viewsets
from Core.models import Showcase, Project
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
        },
        {
            "action": ["retrieve"],
            "principal": "*",
            "effect": "allow",
            "condition": ["is_inside_showcase", "is_creator"]
        },
        {
            "action": ["update","partial_update","destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_creator"
        }
    ]
    
    def is_creator(self, request, view, action) -> bool:
        showcase = view.get_object()
        return request.user == showcase.creator or request.user == showcase.project.creator
    
    def is_inside_project(self, request, view, action) -> bool:
        project = generics.get_object_or_404(Project, id=view.kwargs['id'])
        return (request.user == project.creator or 
                project.users.filter(id=request.user.id).exists())
        
    def is_inside_showcase(self, request, view, action) -> bool:
        showcase = view.get_object()
        return (request.user == showcase.creator or 
                showcase.users.filter(id=request.user.id).exists())



class ShowcaseListCreateView(generics.ListCreateAPIView,
                             viewsets.GenericViewSet):
    """
    list:
    Visualizza la lista delle bacheche.
    
    Visualizza una lista di tutte le bacheche del progetto di cui è stato passato l'id.
    Soltato i partecipanti del progetto possono vedere le bacheche.
    
    ---- ERRORE in "last_message" ----
    L'ultimo messaggio non è una stringa ma è un oggetto formattato in base al tipo del messaggio.
    L'ultimo messaggio può essere un messaggio testuale, un aggiornameto della bacheca ma NON un evento
    
    create:
    Crea una nuova bacheca.
    
    Crea una nuova bacheca nel progetto di cui è stato passato l'id.
    Soltato i partecipanti del progetto possono creare delle bacheche.
    
    ---- ERRORE in "last_message" ----
    L'ultimo messaggio non è una stringa ma è un oggetto formattato in base al tipo del messaggio.
    L'ultimo messaggio può essere un messaggio testuale, un aggiornameto della bacheca ma NON un evento.
    """
    queryset = Showcase.objects.all()
    permission_classes = [IsAuthenticated, ShowcaseAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_serializer_class(self, *args, **kwargs):
        if self.action == "list":
            return ShowcaseReadSerializer
        if self.action == "create":
            return ShowcaseWriteSerializer
    
    def get_project(self):
        project_id = self.kwargs['id']
        return generics.get_object_or_404(Project, id=project_id)
    
    def get_queryset(self):
        return Showcase.objects.filter(project__id=self.kwargs['id']).order_by("created_at")
    
    def perform_create(self, serializer):
        instance = serializer.save(project=self.get_project(),creator=self.request.user)
        instance.users.add(self.request.user)
        
        
        
class ShowcaseRUDView(generics.RetrieveUpdateDestroyAPIView,
                      viewsets.GenericViewSet):
    """
    retrieve:
    Vedi i dati della bacheca.
    
    Vedi tutti i dati della bacheca di cui è stato passato l'id.
    Soltato chi è all'interno della bacheca o il creatore del progetto può vedere 
    questi dati. Endpoints da usare per esempio nella sezione dettagli del progetto.
    
    update:
    Aggiorna i dati di una bacheca.
    
    Aggiorna i dati della bacheca di cui è stato passato l'id, soltato il creatore della bacheca
    o il creatore del progetto può aggiornare i dati della bacheca.
    Endpoints da usare per esempio nella sezione dettagli del progetto per modificare i dati.
    
    partial_update:
    Aggiorna i dati di una bacheca.
    
    Aggiorna i dati della bacheca di cui è stato passato l'id, soltato il creatore della bacheca
    o il creatore del progetto può aggiornare i dati della bacheca.
    Endpoints da usare per esempio nella sezione dettagli del progetto per modificare i dati.
    
    destroy:
    Elimana una bacheca.
    
    Elimna la bacheca di cui è stato passato l'id, soltato il creatore della bacheca
    o il creatore del progetto può eliminare la bacheca.
    """
    queryset = Showcase.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, ShowcaseAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_serializer_class(self, *args, **kwargs):
        if self.action == "retrieve" or self.action == "destroy":
            return ShowcaseReadSerializer
        if self.action == "update" or self.action == "partial_update":
            return ShowcaseWriteSerializer
    
    def perform_update(self, serializer):
        instance = serializer.save()
        self.add_creator_to_users(instance)

    def add_creator_to_users(self, instance):
        if not instance.users.filter(id=instance.creator.id).exists():
            instance.users.add(instance.creator)