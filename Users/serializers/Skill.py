from django.db.models import fields
from rest_framework import serializers
from Core.models import Skill, UserSkill
from Core.models.Users.User import User


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
        
        
class UserSkillListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    type_skill = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserSkill
        exclude = ["user"]
        
    def get_skill(self, instance):
        return instance.skill.name
    
    def get_type(self, instance):
        return instance.skill.type_skill
    
    def get_id(self, instance):
        return instance.skill.id
    
    
class UserSkillCreateSerializer(serializers.ModelSerializer):
    level = serializers.IntegerField(required=True)
    
    class Meta:
        model = UserSkill
        read_only_fields = ["user"]
        fields = "__all__"