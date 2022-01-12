from rest_framework import serializers
from Core.models import TextMessage

class TextMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMessage
        fields = "__all__"