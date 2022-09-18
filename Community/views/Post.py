from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from Core.models import Post, PostComment
from ..serializers.Post import PostSerializer, PostCommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_access_policy import AccessPolicy


class PostCommentAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["update", "partial_update", "destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_author"
        },
        {
            "action": ["create", "list"],
            "principal": "*",
            "effect": "allow",
        },
    ]
    
    def is_author(self, request, view, action) -> bool:
        object = view.get_object()
        return request.user == object.author
    


class PostListView(generics.ListAPIView,
                   viewsets.GenericViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_queryset(self):
        return Post.objects.all()\
                           .select_related('project_question','text_post','news',"author")\
                           .order_by("-updated_at")



class PostCommentListCreateView(generics.ListCreateAPIView,
                                viewsets.GenericViewSet):
    serializer_class = PostCommentSerializer
    queryset = PostComment.objects.all()
    permission_classes = [IsAuthenticated, PostCommentAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_queryset(self):
        return PostComment.objects.filter(post__id=self.kwargs['id'])
    
    def perform_create(self, serializer):
        serializer.save(post=get_object_or_404(Post, id=self.kwargs['id']), 
                        author=self.request.user)
        
        

class PostCommentLikeAPIView(APIView):
    
    def post(self, request, id):
        comment = get_object_or_404(PostComment, id=id)
        if comment.likes.filter(id=request.user.id).exists():
            return Response(data={"msg": "Like già inserito"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        comment.likes.add(request.user)
        comment.save()
        return Response(data={"msg": "Like inserito"}, 
                        status=status.HTTP_201_CREATED)
        
        
    def delete(self, request, id):
        comment = get_object_or_404(PostComment, id=id)
        if not comment.likes.filter(id=request.user.id).exists():
            return Response(data={"msg": "Like non inserito"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        comment.likes.remove(request.user)
        comment.save()
        return Response(data={"msg": "Like eliminato"}, 
                        status=status.HTTP_204_NO_CONTENT)



class PostCommentUpdateDestroyView(generics.UpdateAPIView,
                                   generics.DestroyAPIView,
                                   viewsets.GenericViewSet):
    serializer_class = PostCommentSerializer
    queryset = PostComment.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, PostCommentAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)






