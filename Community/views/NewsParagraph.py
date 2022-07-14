from rest_framework import viewsets, generics
from ..serializers import NewsParagraphSerializer, NewsParagraphImageSerializer
from Core.models import News, NewsParagraphImage, NewsParagraph, Project
from django.shortcuts import get_object_or_404
from rest_access_policy.access_policy import AccessPolicy
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings
from rest_framework.permissions import IsAuthenticated


class NewsParagraphAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "*",
            "effect": "allow"
        },
        {
            "action": ["create", "update", "partial_update"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_author"
        },
        {
            "action": ["destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": ["is_project_creator","is_author"]
        }
    ]
    
    def is_author(self, request, view, action) -> bool:
        news = view.get_object()
        if not isinstance(news, News): news = news.news
        return (news.author == request.user)
    
    def is_project_creator(self, request, view, action) -> bool:
        news = view.get_object().news
        return (news.project.creator == request.user)


class NewsParagraphListCreateView(generics.ListCreateAPIView,
                                  viewsets.GenericViewSet):
    serializer_class = NewsParagraphSerializer
    queryset = NewsParagraph.objects.all()
    permission_classes = [IsAuthenticated, NewsParagraphAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_object(self):
        if not hasattr(self, "news"):
            self.news = get_object_or_404(News, id=self.kwargs['id'])
        return self.news
    
    def get_queryset(self):
        return NewsParagraph.objects.filter(news__id=self.kwargs['id'])
    
    def perform_create(self, serializer):
        serializer.save(news=self.news)


class NewsParagraphUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView,
                                    viewsets.GenericViewSet):
    serializer_class = NewsParagraphSerializer
    queryset = NewsParagraph.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, NewsParagraphAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
