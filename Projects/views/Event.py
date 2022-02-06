from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from ..serializers import EventWriteSerializer, EventReadSerializer, EventTaskSerializer
from Core.models import Event, EventTask, Showcase
from rest_framework.response import Response
from rest_framework import status
from rest_access_policy import AccessPolicy

from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings


class EventAccessPolicy(AccessPolicy):
    statements = [
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
    Soltato i coloro che sono dentro la bacheca possono creare un evento al suo interno.
    Una volta creato l'evento il creatore viene automaticamente aggiunto alla lista dei partecipanti.
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