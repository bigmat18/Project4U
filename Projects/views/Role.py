from rest_framework import generics, mixins
from rest_framework import viewsets
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
            "action": ["destroy", "update", "create"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_creator"
        },
    ]
    
    def is_creator(self, request, view, action) -> bool:
        project = view.get_object()
        return request.user == project.creator
    
    def is_inside_project(self, request, view, action) -> bool:
        project = view.get_object()
        print(project.users)
        return True



class RoleListCreateView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, RoleAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)

    
    def perform_create(self, serializer):
        projectId = self.kwargs['id']
        serializer.save(project=projectId)
    
    
    
class RoleUpdateDestroyView(mixins.UpdateModelMixin,
             mixins.DestroyModelMixin,
             viewsets.GenericViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, RoleAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)