from rest_framework import viewsets, generics
from ..serializers import TextPostSerializer
from Core.models import TextPost, Project
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
    
    
class TextPostCreateView(generics.CreateAPIView,
                         viewsets.GenericViewSet):
    serializer_class = TextPostSerializer
    queryset = TextPost.objects.all()
    permission_classes = [IsAuthenticated]
    
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
    serializer_class = TextPostSerializer
    queryset = TextPost.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "id"