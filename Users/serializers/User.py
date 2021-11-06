from Core.models import User
from rest_framework import serializers
from Users.serializers import UserSkillSerializer


class UserDetailSerializer(serializers.ModelSerializer):
    skills = UserSkillSerializer(source="userskill_set",many=True)
    
    class Meta:
        model = User
        exclude = ["active", "password", "date_joined", 
            "last_login","username","admin"]