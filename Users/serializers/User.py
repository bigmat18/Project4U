from Core.models import User
from rest_framework import serializers
from Users.serializers import UserSkillListSerializer


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["slug", "first_name", "last_name", "image","type_user"]


class UserDetailSerializer(serializers.ModelSerializer):
    skills = UserSkillListSerializer(source="userskill_set",many=True, required=False, read_only=True)
    
    class Meta:
        model = User
        read_only_fields = ["slug", "blocked", "type_user"]
        exclude = ["active", "password", "date_joined", 
            "last_login","username","admin", "user_saved",
            "project_saved","type_vip"]