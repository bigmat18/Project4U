from rest_framework import serializers
from Core.models import Message
from Showcases.serializers import TextMessageSerializer, EventSerializer

class MessageSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Message
        exclude = ["created_at", "showcase", "viewed_by"]
        
    def get_content(self, instance):
        if instance.type_message == "TEXT":
            return TextMessageSerializer(instance=instance.text_message).data
        elif instance.type_message == "EVENT":
            return EventSerializer(instance=instance.event).data