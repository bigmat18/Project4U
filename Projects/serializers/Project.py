from rest_framework import serializers
from Core.models import Project
from .ProjectTag import ProjectTagSerializer


class ProjectSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id","image","name","text","link_site"]


class ProjectSerializerDetail(serializers.ModelSerializer):
    num_swipe = serializers.IntegerField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    tags_list = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Project
        exclude = ["users"]
        extra_kwargs = {
            'tags': {'write_only': True},
        }

    def get_tags_list(self,instance):
        return ProjectTagSerializer(instance=instance.tags,many=True).data