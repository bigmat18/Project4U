from Core.models import Showcase, Message,User
from rest_framework import serializers
from .Message import MessageSerializer
from django.db.models import Q


class UsersShowcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","slug", "first_name", "last_name", "image"]



class ShowcaseWriteSerializer(serializers.ModelSerializer):
    users_list = UsersShowcaseSerializer(source="users", many=True, read_only=True)
    
    class Meta:
        model = Showcase
        fields = ["id","name", "users", "description", "color", "users_list"]
        extra_kwargs = {'users': {'write_only': True}}


class ShowcaseReadSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField(read_only=True)
    last_event = serializers.SerializerMethodField(read_only=True)
    users = UsersShowcaseSerializer(many=True,read_only=True)
    notify = serializers.SerializerMethodField(read_only=True)
    creator = UsersShowcaseSerializer(read_only=True)
        
    class Meta:
        model = Showcase
        exclude = ["project"]

        
    def get_last_event(self, instance):
        last_event = Message.objects.filter(Q(showcase=instance) & Q(type_message="EVENT"))\
                                      .order_by("updated_at")\
                                      .first()
        if not last_event: return last_event
        return MessageSerializer(instance=last_event).data
        
    def get_last_message(self,instance):
        last_message = Message.objects.filter(Q(showcase=instance) & ~Q(type_message="EVENT"))\
                                      .order_by("updated_at")\
                                      .first()
        if not last_message: return last_message
        return MessageSerializer(instance=last_message).data
    
    def get_notify(self, instance) -> int:
        return Message.objects.filter(showcase=instance)\
                              .exclude(viewed_by=self.context['request'].user)\
                              .count()