from Core.models import User, Project
from rest_framework import serializers
from Users.serializers import (UserSkillListSerializer, 
                                ExternalProjectSerializer,
                                UserEducationSerializer)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["slug", "first_name", "last_name", "image","type_user"]


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
    projects = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        read_only_fields = ["slug", "blocked"]
        exclude = ["active", "password", "date_joined", 
            "last_login","username","admin"]
        
    def get_projects(self, instance):
        projects = Project.objects.filter(users=instance)
        projects_list = []
        for project in projects:
            projects_list.append({"id":project.id,
                                  "name":project.name,
                                  "description":project.text,
                                  "image":(project.image if project.image else None)})
        return projects_list
        
        
class CurrentUserImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["image"]