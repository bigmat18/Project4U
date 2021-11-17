from rest_framework import generics, viewsets
from Core.models import Skill
from Users.serializers import SkillSerializer
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings


class SkillListView(generics.ListAPIView,
                    viewsets.GenericViewSet):
    """
    list:
    Lista delle skills
    
    Una lista di tutte le skills
    """
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    permission_classes = []
    if not settings.DEBUG: permission_classes.append(HasAPIKey)


