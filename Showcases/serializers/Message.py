from rest_framework import serializers
from Core.models import Message
from .TextMessage import TextMessageSerializer

class MessageSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Message
        fields = "__all__"
        
    def get_content(self, instance):
        if instance.type_message == "TXT":
            return TextMessageSerializer(instance=instance.message_ptr_id).data