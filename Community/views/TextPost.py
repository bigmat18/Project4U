from rest_framework import viewsets, generics
from ..serializers import TextPostSerializer
from Core.models import TextPost, Project
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_access_policy.access_policy import AccessPolicy


class TextPostAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_inside_project"
        },
        {
            "action": ["retrieve"],
            "principal": "*",
            "effect": "allow",
        },
        {
            "action": ["destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": ["is_author", "is_project_creator"]
        },
        {
            "action": ["destroy", "update", "partial_update"],
            "principal": "*",
            "effect": "allow",
            "condition": ["is_author"]
        },
    ]
    
    def is_inside_project(self, request, view, action) -> bool:
        project = view.get_object()
        return (request.user == project.creator or 
                project.users.filter(id=request.user.id).exists())
        
    def is_author(self, request, view, action) -> bool:
        news = view.get_object()
        return request.user == news.author
    
    def is_project_creator(self, request, view, action) -> bool:
        post = view.get_object()
        return (post.project.creator == request.user)
    
    
    
class TextPostCreateView(generics.CreateAPIView,
                         viewsets.GenericViewSet):
    """
    create:
    Crea un post testuale.
    
    Crea un post testuale all'interno del progetto a cui è stato messo l'id nell'url.
    """
    serializer_class = TextPostSerializer
    queryset = TextPost.objects.all()
    permission_classes = [IsAuthenticated, TextPostAccessPolicy]
    
    def get_object(self):
        if not hasattr(self, "project"): 
            self.project = get_object_or_404(Project, id=self.kwargs['id'])
        return self.project
    
    def perform_create(self, serializer):
        serializer.save(project=self.get_object(), 
                        author=self.request.user)
    


class TextPostUpdateDestroyView(generics.UpdateAPIView,
                                generics.DestroyAPIView,
                                viewsets.GenericViewSet):
    """
    update:
    Aggiorna post testuale.
    
    Aggiorna post testuale. Soltato il creatore del post può eseguire questa operazione.
    
    partial_update:
    Aggiorna parzialmente post testuale.
    
    Aggiorna parzialmente post testuale. Soltato il creatore del post può eseguire questa operazione.
    
    destroy:
    Elimina post testuale.
    
    Elimina post testuale. Soltato il creatore del post ed il creatore del progetto possono eseguire questa operazione.
    """
    serializer_class = TextPostSerializer
    queryset = TextPost.objects.all()
    permission_classes = [IsAuthenticated, TextPostAccessPolicy]
    lookup_field = "id"