from rest_framework import serializers
from Core.models import Message, User
from .TextMessage import TextMessageSerializer
from .Event import EventSerializer


class AuthorMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","secret_key", "first_name", "last_name", "image"]


class MessageSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField(read_only=True)
    author = AuthorMessageSerializer(read_only=True)
    
    class Meta:
        model = Message
        exclude = ["created_at", "showcase", "viewed_by"]
        
    def get_content(self, instance):
        if instance.type_message == "TEXT":
            return TextMessageSerializer(instance=instance.text_message).data
        elif instance.type_message == "EVENT":
            return EventSerializer(instance=instance.event).data