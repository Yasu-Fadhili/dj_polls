
from django.urls import path
from rest_framework.routers import DefaultRouter
from polls.views import PollViewSet, CommentViewSet, VoteViewSet

router = DefaultRouter()
router.register(r"", PollViewSet, basename="polls")
router.register(r"comments", CommentViewSet, basename="comments")
router.register(r"votes", VoteViewSet, basename="votes")


urlpatterns = [
    path("<int:pk>/update/", PollViewSet.as_view({"put": "update_poll"}), name="poll-update"),
    path("<int:pk>/delete/", PollViewSet.as_view({"delete": "delete_poll"}), name="poll-delete"),
    path("comments/<int:pk>/update/", CommentViewSet.as_view({"put": "update_comment"}), name="comment-update"),
    path("comments/<int:pk>/delete/", CommentViewSet.as_view({"delete": "delete_comment"}), name="comment-delete"),
    path("votes/create/", VoteViewSet.as_view({"post": "create_vote"}), name="vote-create"),
    path("votes/<int:pk>/delete/", VoteViewSet.as_view({"delete": "delete_vote"}), name="vote-delete"),
]

urlpatterns += router.urls


