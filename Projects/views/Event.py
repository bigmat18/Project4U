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
            "action": ["create","retrieve"],
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



class EventCreateView(generics.CreateAPIView,
                      viewsets.GenericViewSet):
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
    serializer_class = EventTaskSerializer
    queryset = EventTask.objects.all()
    
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


class EventTaskRUDView(generics.RetrieveUpdateDestroyAPIView,
                       viewsets.GenericViewSet):
    serializer_class = EventTaskSerializer
    queryset = EventTask.objects.all()
    lookup_field = "id"
    