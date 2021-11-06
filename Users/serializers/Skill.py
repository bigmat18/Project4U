from django.db.models import fields
from rest_framework import serializers
from Core.models import Skill, UserSkill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["name", "type_skill"]
        
        
class UserSkillSerializer(serializers.ModelSerializer):
    skill = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
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