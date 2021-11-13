from rest_framework import mixins, viewsets
from Users.serializers import ExternalProjectSerializer
from Core.models import ExternalProject
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework_api_key.permissions import HasAPIKey


class ExternalProjectCUDView(mixins.CreateModelMixin, 
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = ExternalProjectSerializer
    queryset = ExternalProject.objects.all()
    loockup_filds = "id"
    permission_classes = [IsAuthenticated]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)

    def get_queryset(self):
        return ExternalProject.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)