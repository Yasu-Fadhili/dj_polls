from django.urls import path, include

from polls.views import (
    PollViewSet
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", PollViewSet, basename="polls")

urlpatterns = [
    path("", include(router.urls))
]


