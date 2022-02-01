from django.db import models
from ..serializers import ShowcaseSerializer
from rest_framework import generics, viewsets
from Core.models import Showcase, Project, ShowcaseUpdate
from rest_access_policy import AccessPolicy
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema



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


@method_decorator(name="create",
                  decorator=swagger_auto_schema(
                      responses={"201": ShowcaseSerializer},
                      request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                  required=["name"],
                                                  properties={"users":openapi.Schema(type=openapi.TYPE_ARRAY,
                                                                                     items=openapi.Schema(
                                                                                         type=openapi.TYPE_STRING,
                                                                                         description="Mandare l'uuid dell'utente")),
                                                           "name": openapi.Schema(type=openapi.TYPE_STRING,
                                                                                  maxLength=64,
                                                                                  minLength=1),
                                                           "text":openapi.Schema(type=openapi.TYPE_STRING,
                                                                                 maxLength=516)})))
class ShowcaseListCreateView(generics.ListCreateAPIView,
                             viewsets.GenericViewSet):
    """
    list:
    Visualizza la lista delle bacheche.
    
    Visualizza una lista di tutte le bacheche del progetto di cui è stato passato l'id.
    Soltato i partecipanti del progetto possono vedere le bacheche.
    
    ---- ERRORE in "last_message" ----
    L'ultimo messaggio non è una stringa ma è un oggetto formattato in base al tipo del messaggio.
    
    create:
    Crea una nuova bacheca.
    
    Crea una nuova bacheca nel progetto di cui è stato passato l'id.
    Soltato i partecipanti del progetto possono create le bacheche.
    
    ---- ERRORE in "last_message" ----
    L'ultimo messaggio non è una stringa ma è un oggetto formattato in base al tipo del messaggio.
    """
    serializer_class = ShowcaseSerializer
    queryset = Showcase.objects.all()
    permission_classes = [IsAuthenticated, ShowcaseAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_project(self):
        project_id = self.kwargs['id']
        return generics.get_object_or_404(Project, id=project_id)
    
    def get_queryset(self):
        # ---- TEST DI SUBQUERY (DA RIPRENDERE) ---
        # query = Showcase.objects.filter(project__id=self.kwargs['id'])\
        #                         .annotate(last_message=Subquery(queryset=Message.objects\
        #                             .filter(showcase__id=OuterRef('id'))\
        #                             .order_by("-created_at")\
        #                             .values('id')\
        #                             .annotate(type_message=ArrayAgg('type_message')).values('type_message')\
        #                             .annotate(id=ArrayAgg('id')).values('id')\
        #                             [:1]))
        # print(query[0].last_message)
        return Showcase.objects.filter(project__id=self.kwargs['id']).order_by("created_at")
    
    def perform_create(self, serializer):
        instance = serializer.save(project=self.get_project(),creator=self.request.user)
        instance.users.add(self.request.user)
        
        
        
class ShowcaseRUDView(generics.RetrieveUpdateDestroyAPIView,
                      viewsets.GenericViewSet):
    serializer_class = ShowcaseSerializer
    queryset = Showcase.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, ShowcaseAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def perform_update(self, serializer):
        instance = serializer.save()
        self.add_creator_to_users(instance)

    def add_creator_to_users(self, instance):
        if not instance.users.filter(id=instance.creator.id).exists():
            instance.users.add(instance.creator)