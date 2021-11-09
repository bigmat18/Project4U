from Core.models import User
from rest_framework import serializers
from Users.serializers import UserSkillSerializer


class UserListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["slug", "first_name", "last_name", "image","type_user"]


class UserDetailSerializer(serializers.ModelSerializer):
    skills = UserSkillSerializer(source="userskill_set",many=True)
    
    class Meta:
        model = User
        exclude = ["active", "password", "date_joined", 
            "last_login","username","admin", "user_saved",
            "project_saved","type_vip"]