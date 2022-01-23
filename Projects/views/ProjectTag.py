from ..serializers import ProjectTagSerializer
from Core.models import ProjectTag
from rest_framework import generics, viewsets


class ProjectTagListCreateView(generics.ListCreateAPIView,
                               viewsets.GenericViewSet):
    serializer_class = ProjectTagSerializer
    queryset = ProjectTag.objects.all()
