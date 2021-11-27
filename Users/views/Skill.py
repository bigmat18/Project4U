from rest_framework import generics, viewsets
from Core.models import Skill
from Users.serializers import SkillSerializer
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings
import django_filters as filters
from django.contrib.postgres.search import TrigramSimilarity
from rest_access_policy import AccessPolicy


class SkillFilter(filters.FilterSet):
    
    class Meta:
        model = Skill
        fields = ["name"]
        
    def filter_queryset(self, queryset):
        if "name" in self.data:
            result = queryset.annotate(similarity=TrigramSimilarity(
                'name',self.data["name"])).filter(
                    similarity__gte=0.01).order_by("-similarity")
            return result
        return queryset
    
    
    
class SkillAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list"],
            "principal": "*",
            "effect": "allow"
        },
        {
            "action": ["create"],
            "principal": "authenticated",
            "effect": "allow"
        }
    ]


    
class SkillListView(generics.ListAPIView,
                    generics.CreateAPIView,
                    viewsets.GenericViewSet):
    """
    list:
    Lista delle skills
    
    Ritorna una lista di tutte le skills.
    E' possibile fare una ricerca aggiungendo " /?name= " alla fine dell'endpoints (dove = inserire la stringa da cercare).
    La ricerca viene effetuata tramite triagrammi, quindi accetta errori di battituira maiuscole/minuscole differenti, caratteri speciali.
    
    create:
    Crea una nuova skill.
    
    E' possibile creare una nuova skill, è richiesta solo l'autenticazione.
    """
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    permission_classes = [SkillAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    filterset_class = SkillFilter



