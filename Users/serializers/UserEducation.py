from rest_framework import serializers
from Core.models import UserEducation

class UserEducationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserEducation
        exclude = ["user"]