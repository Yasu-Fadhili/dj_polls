

from rest_framework import (
    serializers,
)

from polls.models import (
    Poll,
    Option,
    Vote,
)

class VoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vote
        fields = "__all__"

class OptionSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, required=False)

    class Meta:
        model = Option
        fields = "__all__"

class PollSerializer(serializers.ModelSerializer):
    was_published_recently = serializers.BooleanField(read_only=True)
    options = OptionSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Poll
        fields = "__all__"
    
    def create(self, validated_data):
        return Poll.objects.create(**validated_data)


