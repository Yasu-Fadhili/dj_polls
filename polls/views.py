from django.shortcuts import render

from rest_framework import (
    viewsets,
    views,
    permissions,
    exceptions,
    status,
    response
)
from rest_framework.decorators import action

from polls.serialisers import (
    PollSerializer, OptionSerializer, VoteSerializer, CommentSerializer
)

from polls.models import (
    Poll, Option, Vote, Comment
)

from polls.permissions import IsAuthorOrReadOnly 

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = "id"

    # action for updating a poll
    @action(detail=True, methods=['put'])
    def update_poll(self, request, pk=None):
        poll = self.get_object()
        # Check if the user is the author of the poll
        if poll.author != request.user:
            return response.Response({"detail": "You do not have permission to update this poll."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(poll, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # action for deleting a poll
    @action(detail=True, methods=['delete'])
    def delete_poll(self, request, pk=None):
        poll = self.get_object()
        # Check if the user is the author of the poll
        if poll.author != request.user:
            return response.Response({"detail": "You do not have permission to delete this poll."}, status=status.HTTP_403_FORBIDDEN)

        poll.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(id=self.kwargs["id"])
        if not request.user == poll.author:
            raise exceptions.PermissionDenied("You can not delete this poll")
        return super().destroy(request, *args, **kwargs)



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    # action for updating a comment
    @action(detail=True, methods=['put'])
    def update_comment(self, request, pk=None):
        comment = self.get_object()
        # Check if the user is the author of the comment
        if comment.author != request.user:
            return response.Response({"detail": "You do not have permission to update this comment."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # action for deleting a comment
    @action(detail=True, methods=['delete'])
    def delete_comment(self, request, pk=None):
        comment = self.get_object()
        # Check if the user is the author of the comment
        if comment.author != request.user:
            return response.Response({"detail": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    # action for creating a vote
    @action(detail=False, methods=['post'])
    def create_vote(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # action for deleting a vote
    @action(detail=True, methods=['delete'])
    def delete_vote(self, request, pk=None):
        vote = self.get_object()
        # Check if the user is the author of the vote
        if vote.author != request.user:
            return response.Response({"detail": "You do not have permission to delete this vote."}, status=status.HTTP_403_FORBIDDEN)

        vote.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


