from rest_framework import serializers
from Core.models import TextMessage, MessageFile


class MessageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageFile
        fields = ["file"]


class TextMessageSerializer(serializers.ModelSerializer):
    files = MessageFileSerializer(many=True, read_only=True)
    
    class Meta:
        model = TextMessage
        fields = ["id","text", "files"]