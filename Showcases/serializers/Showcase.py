from Core.models import Showcase
from rest_framework import serializers

class ShowcaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Showcase
        exclude = ["project"]