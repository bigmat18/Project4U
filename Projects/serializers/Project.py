from rest_framework import serializers
from Core.models import Project
from .ProjectTag import ProjectTagSerializer


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id","image","name","description","link_site"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    num_swipe = serializers.IntegerField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = ProjectTagSerializer(many=True,read_only=True,source="tags")
    
    class Meta:
        model = Project
        exclude = ["users"]