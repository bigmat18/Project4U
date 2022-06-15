from rest_framework import serializers
from Core.models import News, NewsParagraph, NewsParagraphImage

class NewsParagraphImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewsParagraphImage
        exclude = ["paragraph"]


class NewsParagraphSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewsParagraph
        fields = "__all__"
        read_only_fields = ('news',)
        

class NewsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = News
        exclude = ["type_post", "view_num", "created_at"]
        read_only_fields = ('created_at', 'updated_at', 'author', 'project', "likes")