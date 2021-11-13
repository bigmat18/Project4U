from rest_framework import serializers
from Core.models import ExternalProject

class ExternalProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalProject
        exclude = ["user"]