from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from Core.models import Project


class ProjectSerializerList(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id","image","name","text","link_site"]


class ProjectSerializerDetail(ModelSerializer):
    num_swipe = serializers.IntegerField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Project
        exclude = ["users","tags"]

