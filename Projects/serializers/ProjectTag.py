from rest_framework import serializers
from Core.models import ProjectTag


class ProjectTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTag
        exclude = ["searches_number"]