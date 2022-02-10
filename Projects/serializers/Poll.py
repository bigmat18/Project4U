from rest_framework import serializers
from Core.models import Poll, PollOption


class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOption
        fields = ["text"]


class PollReadSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True,read_only=True)
    
    class Meta:
        model = Poll
        fields = ["id","anonymus_voters", "name", "text"]
        
        
class PollWriteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Poll
        fields = ["id","anonymus_voters", "name", "text"]