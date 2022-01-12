from rest_framework import serializers
from Core.models import Event

class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = ["date","text"]