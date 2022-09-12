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
    serializer_class = ProjectQuestionSerializer
    queryset = ProjectQuestion.objects.all()
    lookup_field = "slug"
    permission_classes = [IsAuthenticated, QuestionAnswerAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)


class ProjectAnswerCreateView(generics.CreateAPIView,
                              viewsets.GenericViewSet):
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
    serializer_class = ProjectQuestionSerializer
    queryset = ProjectQuestion.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, QuestionAnswerAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)