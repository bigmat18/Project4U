from django.shortcuts import get_object_or_404
from rest_framework import mixins, generics, viewsets
from rest_framework.exceptions import ValidationError
from Core.models import UserProject, Project
from ..serializers import UserProjectUpdateSerializer, UserProjectListSerializer
from django.db import IntegrityError
from rest_framework import status



class UserProjectListCreateView(generics.ListCreateAPIView,
                                viewsets.GenericViewSet):
    serializer_class = UserProjectListSerializer
    queryset = UserProject.objects.all()
    
    def get_queryset(self):
        project_id = self.kwargs['id']
        return UserProject.objects.filter(project=project_id)
    
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
    serializer_class = UserProjectUpdateSerializer
    queryset = UserProject.objects.all()
    lookup_field = "id"