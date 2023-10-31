from django.shortcuts import render

from rest_framework import (
    viewsets,
    views,
    permissions,
    exceptions
)

from polls.serialisers import (
    PollSerializer, OptionSerializer, VoteSerializer
)

from polls.models import (
    Poll, Option, Vote
)


class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(id=self.kwargs["id"])
        if not request.user == poll.author:
            raise exceptions.PermissionDenied("You can not delete this poll")
        return super().destroy(request, *args, **kwargs)

