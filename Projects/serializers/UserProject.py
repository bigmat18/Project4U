from rest_framework import serializers
from Core.models import UserProject
from Core.models.Projects.Role import Role
from .Role import RoleSerializer

class UserProjectListSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=True,read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = UserProject
        fields = "__all__"
        

class UserProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProject
        fields = ["role"]