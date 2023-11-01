from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

import uuid
import datetime

class Poll(models.Model):
    id = models.UUIDField(_("Poll Id"), primary_key=True, unique=True, default=uuid.uuid4)
    author = models.ForeignKey(User, verbose_name=_("Poll author"), on_delete=models.CASCADE)
    question = models.CharField(_("Poll Question"), max_length=255)
    expiry_date = models.DateTimeField(_("Poll Expiry Date"), blank=True, null=True)
    visibility = models.CharField(_("Poll Visibility"), max_length=50, choices=(
        ("public", "Public"),
        ("private", "Private"),
    ), default="public")
    created_at = models.DateTimeField(_("Date Time Published"), auto_now=True)
    updated_at = models.DateTimeField(_("Date Time Updated"), auto_now_add=True)

    def options(self):
        return self.option_set.all()

    def was_published_recently(self):
        now = datetime.timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_at <= now

    def total_votes(self):
        return self.vote_set.count()

    def total_comments(self):
        return self.comment_set.count()

    def get_absolute_url(self):
        return reverse("Poll_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.question

class Option(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=_("Option Poll"), on_delete=models.CASCADE)
    option = models.CharField(_("Option"), max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def total_votes(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.option} on poll {self.poll}"

class Vote(models.Model):
    author = models.ForeignKey(User, verbose_name=_("Vote Author"), on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, verbose_name=_("Poll"), on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Poll Option Vote")
        verbose_name_plural = _("Poll Option Votes")
        unique_together = ("poll", "author")

    def __str__(self):
        return f"{self.author} voted {self.option} on {self.poll}"

class Comment(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=_("Poll"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("Poll Author"), on_delete=models.CASCADE)
    content = models.TextField(_("Poll Comment"), max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"{self.content[:50]}"

