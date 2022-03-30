from Core.models import User
from rest_framework import serializers
from Projects.serializers import ProjectListSerializer
from Users.serializers import (UserSkillListSerializer, 
                                ExternalProjectSerializer,
                                UserEducationSerializer)


class UsersListSerializer(serializers.ModelSerializer):
    skills = UserSkillListSerializer(source='user_skill',many=True,read_only=True)
    class Meta:
        model = User
        fields = ["id","slug", "first_name", "last_name", "image", "skills"]


class UsersDetailsSerializer(serializers.ModelSerializer):
    skills = UserSkillListSerializer(source="userskill_set",many=True, 
                                     required=False, read_only=True)
    external_projects = ExternalProjectSerializer(many=True, read_only=True)
    educations = UserEducationSerializer(many=True,read_only=True)
    
    class Meta:
        model = User
        read_only_fields = ["blocked", "slug"]
        exclude = ["active", "password", "date_joined", 
                   "last_login","username","admin", "user_saved",
                   "project_saved","type_vip","secret_key"]
        

class CurrentUserDetailsSerializer(UsersDetailsSerializer):
    projects = ProjectListSerializer(read_only=True,many=True)
    
    class Meta:
        model = User
        read_only_fields = ["secret_key", "blocked", "slug"]
        exclude = ["active", "password", "date_joined", 
                   "last_login","username","admin"]
        
        
class CurrentUserImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["image"]
        
        
class CurrentUserInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id","image", "first_name","last_name", 
                  "date_birth", "type_vip", "type_user"]