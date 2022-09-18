from rest_framework import viewsets, generics
from ..serializers import ProjectQuestionSerializer, ProjectAnswerSerializer
from Core.models import ProjectQuestion, ProjectAnswer, Project
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings
from rest_access_policy import AccessPolicy


class QuestionAnswerAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["update", "partial_update", "destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_author"
        },
        {
            "action": ["create"],
            "principal": "*",
            "effect": "allow",
        },
    ]
    
    def is_author(self, request, view, action) -> bool:
        object = view.get_object()
        return request.user == object.author



class ProjectQuestionCreateView(generics.CreateAPIView,
                                viewsets.GenericViewSet):
    """
    create:
    Crea una domanda.
    
    Crea una domanda per il progetto di cui è stato passato l'id.
    """
    serializer_class = ProjectQuestionSerializer
    queryset = ProjectQuestion.objects.all()
    permission_classes = [IsAuthenticated, QuestionAnswerAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def perform_create(self, serializer):
        serializer.save(project=get_object_or_404(Project, id=self.kwargs['id']),
                        author=self.request.user)



class ProjectQuestionUpdateDestroyView(generics.UpdateAPIView,
                                       generics.DestroyAPIView,
                                       viewsets.GenericViewSet):
    """
    update:
    Aggionrna una domanda.
    
    Aggiorna tutti dati della domanda di cui è stato passato l'slug. Soltato il creatore della domanda può eseguire questa
    operazioni.
    
    partial_update:
    Aggiorna una domanda.
    
    Aggiorna alcuni dati della domanda di cui è stato passato l'slug. Soltato il creatore della domanda può eseguire questa
    operazioni.
    
    detroy:
    Elimina una domanda.
    
    Elimina la domanda di cui è stato passato lo slug. Solato il creatore della domanda può eseguire questa operazione.
    """
    serializer_class = ProjectQuestionSerializer
    queryset = ProjectQuestion.objects.all()
    lookup_field = "slug"
    permission_classes = [IsAuthenticated, QuestionAnswerAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)



class ProjectAnswerCreateView(generics.CreateAPIView,
                              viewsets.GenericViewSet):
    """
    create:
    Crea una risposta ad una domanda.
    
    Crea una risposta alla domanda di cui è stato passato l'id.
    """
    serializer_class = ProjectAnswerSerializer
    queryset = ProjectAnswer.objects.all()
    permission_classes = [IsAuthenticated, QuestionAnswerAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def perform_create(self, serializer):
        serializer.save(question=get_object_or_404(ProjectQuestion, id=self.kwargs['id']),
                        author=self.request.user)


class ProjectAnswerUpdateDestroyView(generics.UpdateAPIView,
                                     generics.DestroyAPIView,
                                     viewsets.GenericViewSet):
    """
    update:
    Aggiorna una risposta.
    
    Aggiorna tutti dati della risposta di cui è stato passato l'id. Soltato il creatore della risposta può eseguire questa
    operazioni.
    
    partial_update:
    Aggiorna una risposta.
    
    Aggiorna alcuni dati della risposta di cui è stato passato l'id. Soltato il creatore della risposta può eseguire questa
    operazioni.
    
    detroy:
    Elimina una risposta.
    
    Elimina la risposta di cui è stato passato lo id. Solato il creatore della risposta può eseguire questa operazione.
    """
    serializer_class = ProjectQuestionSerializer
    queryset = ProjectQuestion.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, QuestionAnswerAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)