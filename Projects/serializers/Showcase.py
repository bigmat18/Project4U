from Core.models import Showcase, Message,User
from rest_framework import serializers
from .Message import MessageSerializer
from django.db.models import Q


class UserShowcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","secret_key", "first_name", "last_name", "image"]

class ShowcaseSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField(read_only=True)
    last_event = serializers.SerializerMethodField(read_only=True)
    users_list = UserShowcaseSerializer(many=True,source="users",read_only=True)
    notify = serializers.SerializerMethodField(read_only=True)
    creator = UserShowcaseSerializer(read_only=True)
        
    class Meta:
        model = Showcase
        exclude = ["project"]
        extra_kwargs = {
            'users': {'write_only': True},
        }
        
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