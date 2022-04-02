from rest_framework import serializers
from Core.models import TextPost

class TextPostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TextPost
        fields = ["text"]