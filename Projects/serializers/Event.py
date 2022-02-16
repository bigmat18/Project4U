from rest_framework import serializers
from Core.models import Event, EventTask, User


class EventPartecipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "secret_key", "image"]


class EventTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTask
        fields = ["checked", "name", "id"]
        read_only_fields = ["checked"]


class EventReadSerializer(serializers.ModelSerializer):
    tasks = EventTaskSerializer(many=True, read_only=True)
    partecipants = EventPartecipantsSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = ["started_at","ended_at","description","partecipants","tasks"]
        
      
class EventWriteSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Event
        fields = ["started_at","ended_at","description","partecipants","id"]
        