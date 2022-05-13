from django.http import QueryDict
from Core.models import Showcase, Message,User
from rest_framework import serializers
from .Message import MessageSerializer
from django.db.models import Q
from rest_framework.request import Request


class UsersShowcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","slug", "first_name", "last_name", "image"]


class ShowcaseWriteSerializer(serializers.ModelSerializer):
    users_list = UsersShowcaseSerializer(source="users", many=True, read_only=True)
    is_creator = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Showcase
        fields = ["id","name", "users", "description", "color", "users_list","is_creator"]
        extra_kwargs = {'users': {'write_only': True}}
        
    def get_is_creator(self, instance):
        return instance.creator == self.context['request'].user


class ShowcaseReadSerializer(serializers.ModelSerializer):
    creator = UsersShowcaseSerializer(read_only=True)
        
    class Meta:
        model = Showcase
        exclude = ["project", "created_at"]
                              
             
             
class CustomShowcaseSerializer():
    def __init__(self, instance, request: Request, many: bool = False) -> None:
        self.instance = instance
        self.request = request
        self.many = many
        
    @property
    def data(self):
        if self.many:
            data = []
            for showcase in self.instance:
                data.append(self.get_showcase(showcase))
        else: data = self.get_showcase(self.instance)
        return data
    
    def get_showcase(self,showcase):        
        return {
            'id': showcase.id,
            'updated_at': showcase.updated_at,
            'name': showcase.name,
            'description': showcase.description,
            'color': showcase.color,
            'is_creator': self.get_is_creator(showcase)
        }
        
    def get_messages_queryset(self, showcase) -> QueryDict:
        return Message.objects.filter(Q(showcase=showcase))\
                              .select_related('author','text_message','event','showcase_update','poll')\
                              .order_by("updated_at")
        
    def get_last_message_serializer(self, messages: QueryDict) -> MessageSerializer:
        for message in messages:
            if message.type_message != "EVENT":
                return MessageSerializer(instance=message).data
        return None
    
    def get_last_event_serializer(self, messages: QueryDict) -> MessageSerializer:
        for message in messages:
            if message.type_message == "EVENT":
                return MessageSerializer(instance=message).data
        return None
    
    def get_notify(self, showcase: Showcase) -> int:
        return Message.objects.filter(showcase=showcase)\
                              .exclude(viewed_by=self.request.user)\
                              .count()
                              
    def get_is_creator(self,showcase):
        return self.request.user == showcase.creator