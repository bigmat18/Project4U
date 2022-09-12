from rest_framework import serializers
from Core.models import ProjectAnswer, ProjectQuestion


class ProjectQuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectQuestion
        fields = ["slug", "content"]


class ProjectAnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectAnswer
        fields = ["author", "content", "updated_at"]