from rest_framework import serializers
from Core.models import Post, PostComment, User
from Community.serializers import NewsSerializer, ProjectQuestionSerializer, TextPostSerializer


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","slug", "first_name", "last_name", "image"]


class PostCommentSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    author = UserPostSerializer(read_only=True)
    
    class Meta:
        model = PostComment
        exclude = ["post", "created_at"]
        
    def get_likes(self,instance):
        return instance.likes.all().count()


class PostSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    author = UserPostSerializer()
    
    class Meta:
        model = Post
        exclude = ["view_num", "created_at"]
        
    def get_content(self, instance):
        if instance.type_post == "NEWS":
            return NewsSerializer(instance=instance.news).data
        elif instance.type_post == "QUESTION":
            return ProjectQuestionSerializer(instance=instance.project_question).data
        elif instance.type_post == "TEXT":
            return TextPostSerializer(instance=instance.text_post).data
        
    def get_likes(self,instance):
        return instance.likes.all().count()