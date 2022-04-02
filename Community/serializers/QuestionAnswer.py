from rest_framework import serializers
from Core.models import ProjectAnswer, ProjectQuestion


class ProjectQuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectQuestion
        fields = ["slug", "question"]


class ProjectAnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectAnswer
        fields = ["author", "answer", "updated_at"]