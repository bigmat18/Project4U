from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from Core.models import Skill, UserSkill, User
from Users.serializers import SkillSerializer, UserSkillCreateSerializer


class SkillListSerializer(generics.ListAPIView,
                          viewsets.GenericViewSet):
    """
    list:
    Lista delle skills
    
    Una lista di tutte le skills
    """
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    permission_classes = [IsAuthenticated]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    
    
    
class UserSkillCreateView(generics.CreateAPIView,
                          viewsets.GenericViewSet):
    """
    create:
    Aggiungi una skill all'utente
    
    Permette di aggiungere una skill con il livello all'utente a cui è riferito lo slug nell'url
    """
    serializer_class = UserSkillCreateSerializer
    queryset = UserSkill.objects.all()
    permission_classes = [IsAuthenticated]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def perform_create(self, serializer):
        slug = self.kwargs.get("slug")
        user = User.objects.get(slug=slug)
        serializer.save(user=user)
    
    