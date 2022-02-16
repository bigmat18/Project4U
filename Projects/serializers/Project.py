from rest_framework import serializers
from Core.models import Project,ProjectTag, User


class UsersProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","secret_key", "first_name", "last_name", "image"]


class ProjectTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTag
        exclude = ["searches_number"]


class ProjectListSerializer(serializers.ModelSerializer):
    tags = ProjectTagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ["id","image","name","description","link_site", "tags"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    num_swipe = serializers.IntegerField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = ProjectTagSerializer(many=True,read_only=True)
    users = UsersProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"