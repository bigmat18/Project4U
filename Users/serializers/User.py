from Core.models import User, Project
from rest_framework import serializers
from django.db.models import Q
from Projects.serializers import ProjectListSerializer
from Users.serializers import (UserSkillListSerializer, 
                                ExternalProjectSerializer,
                                UserEducationSerializer)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","slug", "first_name", "last_name", "image"]


class UserDetailSerializer(serializers.ModelSerializer):
    skills = UserSkillListSerializer(source="userskill_set",many=True, 
                                     required=False, read_only=True)
    external_projects = ExternalProjectSerializer(many=True, read_only=True)
    educations = UserEducationSerializer(many=True,read_only=True)
    
    class Meta:
        model = User
        read_only_fields = ["slug", "blocked"]
        exclude = ["active", "password", "date_joined", 
            "last_login","username","admin", "user_saved",
            "project_saved","type_vip"]
        

class CurrentUserSerializer(UserDetailSerializer):
    projects = ProjectListSerializer(read_only=True,many=True)
    
    class Meta:
        model = User
        read_only_fields = ["slug", "blocked"]
        exclude = ["active", "password", "date_joined", 
            "last_login","username","admin"]
        
        
class CurrentUserImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["image"]