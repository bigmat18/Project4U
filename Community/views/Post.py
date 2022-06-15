from rest_framework import viewsets, generics
from Core.models import Post, PostComment


class PostListView(generics.ListAPIView,
                   viewsets.GenericViewSet):
    pass


class PostCommentCreateView(generics.CreateAPIView,
                            viewsets.GenericViewSet):
    pass


class PostCommentUpdateDestroyCreateView(generics.CreateAPIView,
                                         viewsets.GenericViewSet):
    pass






