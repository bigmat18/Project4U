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
        exclude = ["project", "created_at"]

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
        messages = self.get_messages_queryset(showcase)
        
        return {
            'id': showcase.id,
            'updated_at': showcase.updated_at,
            'name': showcase.name,
            'users': UsersShowcaseSerializer(instance=showcase.users, many=True).data,
            'description': showcase.description,
            'color': showcase.color,
            'notify': self.get_notify(showcase),
            'last_message': self.get_last_message_serializer(messages),
            'last_event': self.get_last_event_serializer(messages)
        }
        
    def get_messages_queryset(self, showcase) -> QueryDict:
        return Message.objects.filter(Q(showcase=showcase))\
                              .select_related('author','text_message','event','showcase_update','poll')\
                              .prefetch_related('event__tasks', 'text_message__files')\
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