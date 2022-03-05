from gc import get_objects
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from ..serializers import EventWriteSerializer, EventReadSerializer, EventTaskSerializer
from Core.models import Event, EventTask, Showcase, Project
from rest_framework.response import Response
from rest_framework import status
from rest_access_policy import AccessPolicy

from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings
from django.db.models import Q


class EventAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_inside_project"
        },
        {
            "action": ["create"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_inside_showcase"
        },
        {
            "action": ["update","partial_update","destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": ["is_author"]
        }
    ]
    
    def is_inside_project(self, request, view, action) -> bool:
        project = view.get_object()
        return (request.user == project.creator or 
                project.users.filter(id=request.user.id).exists())
    
    def is_author(self, request, view, action) -> bool:
        event = view.get_object()
        return request.user == event.author
        
    def is_inside_showcase(self, request, view, action) -> bool:
        showcase = view.get_object()
        return (request.user == showcase.creator or 
                showcase.users.filter(id=request.user.id).exists())
        
        
class EventTaskAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create","destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_author"
        },
        {
            "action": ["update","partial_update"],
            "principal": "*",
            "effect": "allow",
            "condition": ["is_inside_event"]
        }
    ]
    
    def is_author(self, request, view, action) -> bool:
        event = view.get_object().event
        return request.user == event.author
        
    def is_inside_event(self, request, view, action) -> bool:
        event = view.get_object().event
        return (request.user == event.author or 
                event.partecipants.filter(id=request.user.id).exists())



class EventCreateView(generics.CreateAPIView,
                      viewsets.GenericViewSet):
    """
    create:
    Crea un nuovo evento.
    
    Crea un nuovo evento all'iterno della bacheca della quale è stato passato l'id.
    Soltato coloro che sono dentro la bacheca possono creare un evento al suo interno.
    Una volta creato l'evento il creatore viene automaticamente aggiunto alla lista dei partecipanti.
    E' inoltre possibile mandare insieme all'evento una lista "tasks": [...] con all'interno una lista di 
    tasks da aggiungere all'evento in seguito alla creazione (con una lista di task si intende una lista di strighe che 
    indentificano il testo della task)
    """
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, EventAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_serializer_class(self, *args, **kwargs):
        if self.action == "list":
            return EventReadSerializer
        if self.action == "create":
            return EventWriteSerializer
    
    def get_object(self):
        return get_object_or_404(Showcase, id=self.kwargs['id'])
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED and "tasks" in request.data:
            for task in dict(request.data)['tasks']:
                event = get_object_or_404(Event, id=response.data['id'])
                EventTask.objects.create(event=event, name=task)
        return response
    
    def perform_create(self, serializer):
        instance = serializer.save(showcase=self.get_object(), 
                                   type_message = "EVENT",
                                   author=self.request.user)
        instance.partecipants.add(self.request.user)
        instance.viewed_by.add(self.request.user)
    
    
    
class EventUpdateDestroyView(generics.UpdateAPIView,
                             generics.DestroyAPIView,
                             viewsets.GenericViewSet):
    """
    update:
    Aggiorna un evento.
    
    Aggiorna i dati dell'evento cui è stato passato l'id. Soltanto
    il creatore dell'evento può modificarlo.
    
    partial_update:
    Aggiorna un evento parzialemente.
    
    Aggiorna i dati dell'evento parzialemente (cioè non è obbligatorio invare tutti i dati) 
    cui è stato passato l'id. Soltanto il creatore dell'evento può modificarlo.
    
    destroy:
    Elimina un evento.
    
    Elimina l'evento di cui è stato passato l'id. Soltaot il creatore dell'evento lo pò eliminare.
    """
    lookup_field = "id"
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, EventAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_serializer_class(self, *args, **kwargs):
        if self.action == "retrieve" or self.action == "destroy":
            return EventReadSerializer
        if self.action == "update" or self.action == "partial_update":
            return EventWriteSerializer
    


class EventTaskCreateView(generics.CreateAPIView,
                          viewsets.GenericViewSet):
    """
    create:
    Crea una task di un evento.
    
    Crea una o più task legate all'evento di cui è stato passato l'id nell'url.
    Soltato si si è i creatori dell'evento si possono creare task.
    E' possibile anche mandare una lista di task scrivendo [{dati task..},{....}]
    """
    serializer_class = EventTaskSerializer
    queryset = EventTask.objects.all()
    permission_classes = [IsAuthenticated, EventTaskAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_object(self):
        return get_object_or_404(Event, id=self.kwargs['id'])
    
    def create(self, request, *args, **kwargs):
        response = []
        if isinstance(request.data, list):
            for task in request.data:
                serializer = self.get_serializer(data=task)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                response.append(serializer.data)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(event=self.get_object())



class EventTaskUpdateDestroyView(generics.UpdateAPIView,
                                 generics.DestroyAPIView,
                                 viewsets.GenericViewSet):
    """
    update:
    Aggiorna una task di un evento.
    
    Aggiorna i dati di una task di un evento. Soltato se sei dentro l'evento
    puoi aggiornare la task.
    
    partial_update:
    Aggiorna una task di un evento.
    
    Aggiorna i dati di una task di un evento. Soltato se sei dentro l'evento
    puoi aggiornare la task.
    
    destroy:
    Elimina una task di un evento
    
    Elimina una task definitivamente da un evento. Solato il creatore dell'evento
    può eliminare una task.
    """
    serializer_class = EventTaskSerializer
    queryset = EventTask.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, EventTaskAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    
    
class EventInProjectListView(generics.ListAPIView,
                             viewsets.GenericViewSet):
    """
    list:
    Restituisce liste eventi per progetto.
    
    Restituisce una lista di tutti gli eventi del proggetto per il quale è stato
    passato l'id nell'url ed in cui l'utente che ha fatto la richiesta è fra i partecipanti oppure
    è il creatore.
    Soltato se si è dentro il progetto si può effettuare questa richiesta
    """
    serializer_class = EventReadSerializer
    permission_classes = [IsAuthenticated, EventAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_object(self):
        return get_object_or_404(Project, id=self.kwargs['id'])
    
    def get_queryset(self):
        return Event.objects.filter(showcase__project__id=self.kwargs['id'])\
                            .filter(Q(partecipants=self.request.user) | Q(author=self.request.user))\
                            .order_by("started_at")
    

class EventForUserListView(generics.ListAPIView,
                           viewsets.GenericViewSet):
    """
    list:
    Restituisce una lista di tutti gli eventi di un utente.
    
    Restituisce una lista con tutti gli eventi di tutti i progetti dell'utente loggato (in cui l'utente
    è o un partecipante dell'evento oppure è il creatore).
    Per effettuare questa richiesta è sufficente essere loggato.
    """
    serializer_class = EventReadSerializer
    permission_classes = [IsAuthenticated]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_queryset(self):
        return Event.objects.filter(Q(partecipants=self.request.user) | Q(author=self.request.user))\
                            .order_by("started_at")