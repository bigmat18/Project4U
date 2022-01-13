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
        if bool(instance.user.image): image = instance.user.image.url
        else: image = None
        return {"name": instance.user.full_name,
                "image": image}
        

class UserProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProject
        fields = ["role"]