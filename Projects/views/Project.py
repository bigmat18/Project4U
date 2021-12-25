from rest_framework.viewsets import ModelViewSet
from Core.models import Project
from ..serializers import ProjectSerializer
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated]
