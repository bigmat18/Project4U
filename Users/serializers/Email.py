from rest_framework import serializers
from Core.models import Email

class EmailSerializer(serializers.ModelSerializer):
    added_at = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = Email
        fields = "__all__"

    def get_added_at(self, instance):
        return instance.added_at.strftime('%d %B %Y')