from ..serializers import ShowcaseSerializer
from rest_framework import generics, viewsets
from Core.models import Showcase, Project, Message

class ShowcaseListCreateView(generics.ListCreateAPIView,
                             viewsets.GenericViewSet):
    serializer_class = ShowcaseSerializer
    queryset = Showcase.objects.all()
    
    def get_project(self):
        project_id = self.kwargs['id']
        return generics.get_object_or_404(Project, id=project_id)
    
    def get_queryset(self):
        return Showcase.objects.filter(project__id=self.kwargs['id'])
    
    def perform_create(self, serializer):
        instance = serializer.save(project=self.get_project())
        instance.users.add(self.request.user)