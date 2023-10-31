

from rest_framework import (
    serializers,
)

from polls.models import (
    Poll,
    Option,
    Vote,
    Comment
)

class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = (
            "id",
            "author",
            "poll",
            "option"
        )

class OptionSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, required=False)

    class Meta:
        model = Option
        fields = (
            "id",
            "option"
        )

class PollSerializer(serializers.ModelSerializer):
    #was_published_recently = serializers.BooleanField(read_only=True)
    choices = OptionSerializer(many=True, read_only=True, required=False)
    #choices = OptionSerializer()

    class Meta:
        model = Poll
        fields = (
            "id",
            "question",
            "choices",
            "expiry_date",
            "visibility",
            "created_at",
            "updated_at"
        )
    
    def create(self, validated_data):
        return Poll.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "poll",
            "author",
            "content",
            "created_at"
        )

