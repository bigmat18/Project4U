from rest_framework import serializers
from Core.models import Post, PostComment
# from Community.serializers import NewsListSerializer, ProjectQuestionSerializer, TextPostSerializer


# class PostCommentSerializer(serializers.ModelSerializer):
#     likes = serializers.SerializerMethodField(read_only=True)
    
#     class Meta:
#         model = PostComment
#         exclude = ["post"]
        
#     def get_likes(self,instance):
#         return instance.likes.all().count()


# class PostSerializer(serializers.ModelSerializer):
#     content = serializers.SerializerMethodField(read_only=True)
#     likes = serializers.SerializerMethodField(read_only=True)
#     comments = PostCommentSerializer(many=True)
    
#     class Meta:
#         model = Post
#         exclude = ["views_num", "created_at"]
        
#     def get_content(self, instance):
#         if instance.type_message == "NEWS":
#             return NewsListSerializer(instance=instance.news).data
#         elif instance.type_message == "QUESTION":
#             return ProjectQuestionSerializer(instance=instance.question).data
#         elif instance.type_message == "TEXT":
#             return TextPostSerializer(instance=instance.text_post).data
        
#     def get_likes(self,instance):
#         return instance.likes.all().count()