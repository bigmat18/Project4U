from rest_framework import viewsets, generics
from ..serializers import NewsDetailSerializer, NewsListSerializer, NewsParagraphSerializer
from Core.models import News, NewsParagraphImage, NewsParagraph


class NewsCreateView(generics.CreateAPIView,
                     viewsets.GenericViewSet):
    pass


class NewsParagraphCreateView(generics.CreateAPIView,
                              viewsets.GenericViewSet):
    pass


class NewsRUDView(generics.RetrieveUpdateDestroyAPIView,
                  viewsets.GenericViewSet):
    pass


class NewsParagraphUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView,
                                     viewsets.GenericViewSet):
    pass