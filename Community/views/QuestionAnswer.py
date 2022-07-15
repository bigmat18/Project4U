from rest_framework import viewsets, generics
from ..serializers import ProjectQuestionSerializer, ProjectAnswerSerializer
from Core.models import ProjectQuestion, ProjectAnswer


class ProjectQuestionCreateView(generics.CreateAPIView,
                                viewsets.GenericViewSet):
    pass


class ProjectQuestionUpdateDestroyView(generics.UpdateAPIView,
                                       generics.DestroyAPIView,
                                       viewsets.GenericViewSet):
    pass


class ProjectAnswerCreateView(generics.CreateAPIView,
                              viewsets.GenericViewSet):
    pass


class ProjectAnswerUpdateDestroyView(generics.UpdateAPIView,
                                     generics.DestroyAPIView,
                                     viewsets.GenericViewSet):
    pass