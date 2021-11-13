from rest_framework import generics, viewsets, mixins
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from Core.models import Skill, UserSkill
from Users.serializers import SkillSerializer, UserSkillCreateSerializer
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError


class SkillListView(generics.ListAPIView,
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


    
class UserSkillCUDView(mixins.CreateModelMixin,mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    create:
    Aggiungi una skill all'utente
    
    Permette di aggiungere una skill con il livello all'utente a cui è riferito lo slug nell'url
    
    update:
    Aggiorna i dati di una skill
    
    Aggiorna i dati della skill, la skilla da aggiornare viene decisa in base all'id della skill messo nell'url ({skill} = id skill)
    
    destroy:
    Rimuovi una skill da un utente
    
    Rimuovi una skill da un utente, la skilla da eliminare viene decisa in base all'id della skill messo nell'url ({skill} = id skill)
    """
    serializer_class = UserSkillCreateSerializer
    queryset = UserSkill.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "skill"
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_queryset(self):
        skill = self.kwargs.get("skill")
        return UserSkill.objects.filter(skill=skill).filter(user=self.request.user)
    
    def perform_create(self, serializer):
        try: serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"Error":"è già stata abbinata questa skill a questo utente"})
    
    
    