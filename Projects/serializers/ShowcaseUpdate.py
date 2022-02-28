from rest_framework import serializers
from Core.models import ShowcaseUpdate

class ShowcaseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowcaseUpdate
        fields = ["id","description", "type_update"]