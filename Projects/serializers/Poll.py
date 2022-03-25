from rest_framework import serializers
from Core.models import Poll, PollOption, User


class PollOptionVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id', 'slug', 'image']


class PollOptionSerializer(serializers.ModelSerializer):
    num_votes = serializers.SerializerMethodField(read_only=True)
    voters = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = PollOption
        fields = ["text", "num_votes", "voters"]
        
    def get_num_votes(self, instance):
        return instance.votes.count()
    
    def get_voters(self, instance):
        if not instance.poll.anonymus_voters:
            return PollOptionVotesSerializer(instance=instance.votes, many=True).data
        else: return None


class PollReadSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True,read_only=True)
    
    class Meta:
        model = Poll
        fields = ["id","anonymus_voters", "name", "text", "options"]
        
        
class PollWriteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Poll
        fields = ["id","anonymus_voters", "name", "text", "updated_at"]