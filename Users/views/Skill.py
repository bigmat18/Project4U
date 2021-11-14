from rest_framework import generics, viewsets, mixins
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


    
class UserSkillCUDView(mixins.CreateModelMixin,mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    create:
    Aggiungi una skill all'utente
    
    Permette di aggiungere una skill con il livello all'utente a cui è riferito lo slug nell'url
    
    update:
    Aggiorna i dati di una skill
    
    Aggiorna i dati della skill, la skill da aggiornare viene decisa in base all'id della skill messo nell'url ({skill} = id skill)
    
    destroy:
    Rimuovi una skill da un utente
    
    Rimuovi una skill da un utente, la skill da eliminare viene decisa in base all'id della skill messo nell'url ({skill} = id skill)
    """
    serializer_class = UserSkillCreateSerializer
    queryset = UserSkill.objects.all()
    lookup_field = "skill"
    
    def get_queryset(self):
        skill = self.kwargs.get("skill")
        return UserSkill.objects.filter(skill=skill).filter(user=self.request.user)
    
    def perform_create(self, serializer):
        try: serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"Error":"è già stata abbinata questa skill a questo utente"})
    
    
    