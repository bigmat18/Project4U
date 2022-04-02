from rest_framework import serializers
from Core.models import News, NewsParagraph, NewsParagraphImage
from ..serializers import PostCommentSerializer

class NewsParagraphImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewsParagraphImage
        exclude = ["paragraph"]


class NewsParagraphSerializer(serializers.ModelSerializer):
    images = NewsParagraphImageSerializer(many=True)
    
    class Meta:
        model = NewsParagraph
        exclude = ["news"]


class NewsDetailSerializer(serializers.ModelSerializer):
    paragraphs = NewsParagraphSerializer(many=True)
    comments = PostCommentSerializer(many=True)
    
    class Meta:
        model = News
        fields = ["title", "image", "slug", "content", "author", "updated_at",
                  "likes", "comments"]
        

class NewsListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = News
        fields = ["title", "image", "slug", "content"]