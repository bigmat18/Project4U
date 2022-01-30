from django.shortcuts import get_object_or_404
from Core.models.Projects.Project import Project
from ..serializers import ProjectTagSerializer
from Core.models import ProjectTag
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status

class ProjectTagCreateView(generics.CreateAPIView,
                           viewsets.GenericViewSet):
    """
    create:
    Crea tags progetto.
    
    Crea un nuovo tags progetto.
    """
    serializer_class = ProjectTagSerializer
    queryset = ProjectTag.objects.all()
    
    def add_or_create_tag(self,tag_name,project):
        tag = ProjectTag.objects.filter(name=tag_name)
        if not tag.exists():
            new_tag = ProjectTag.objects.create(name=tag_name)
            project.tags.add(new_tag)
        else: project.tags.add(tag[0])

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs['id'])
        if isinstance(request.data, list):
            for tag in request.data:
                self.add_or_create_tag(tag_name=tag['name'],project=project)
        else: self.add_or_create_tag(tag_name=request.data['name'],project=project)
        return Response(status=status.HTTP_201_CREATED)