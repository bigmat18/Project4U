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
    Crea/aggiungi tags ad un progetto
    
    Questo endponts permette di andare a creare ed aggiungere o solo aggiungere un tag ad il 
    progetto di cui si è passato l'id, infatti data una lista di nomi di tag (oppure un singolo tag, infatti 
    è possibile mandare sia una lista che un singolo) viene controllato se esiste già un tag con quel nome nel db
    e nel caso contrario viene creato e poi in qualsiasi caso viene aggiungo al progetto.
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