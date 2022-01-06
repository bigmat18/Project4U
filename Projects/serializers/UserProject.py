from rest_framework import serializers
from Core.models import UserProject
from .Role import RoleSerializer


class UserProjectListSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=True,read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    user_detail = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = UserProject
        fields = "__all__"
        
    def get_user_detail(self,instance):
        return {"name": instance.user.full_name, 
                "image": (instance.user.image if instance.user.image else None)}
        

class UserProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProject
        fields = ["role"]