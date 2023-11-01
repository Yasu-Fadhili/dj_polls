from django.contrib.auth.models import User

from rest_framework import (
    serializers,
)

from polls.models import (
    Poll,
    Option,
    Vote,
    Comment
)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
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
    #votes = VoteSerializer(many=True, required=False)

    class Meta:
        model = Option
        fields = (
            "id",
            "option",
            "total_votes"
        )

class PollSerializer(serializers.ModelSerializer):
    #was_published_recently = serializers.BooleanField(read_only=True)
    options = OptionSerializer(many=True, read_only=True, required=False)
    author = AuthorSerializer(read_only=True)
    #choices = OptionSerializer()

    class Meta:
        model = Poll
        fields = (
            "id",
            "author",
            "question",
            "options",
            "expiry_date",
            "visibility",
            "total_votes",
            "total_comments",
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

