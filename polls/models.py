from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

import uuid


class Poll(models.Model):
    id = models.UUIDField(_("Poll Id"), 
                          primary_key=True,
                          unique=True,
                          default=uuid.uuid4)
    question = models.CharField(_("Poll Question"), max_length=255)
    expiry_date = models.DateTimeField(_("Poll Expiry Date"), auto_now_add=True)
    visibility = models.CharField(_("Poll Visibility"), max_length=50,
                                  choices=(
                                      ("public", "Public"),
                                      ("private", "Private")
                                      ), default="public")
    
    def total_votes(self):
        return Vote.objects.filter(poll=self).count()
    
    def total_comments(self):
        return Comment.objects.filter(poll=self).count()
    
    def get_absolute_url(self):
        return reverse("Poll_detail", kwargs={"pk": self.pk})
    
    def __str__(self) -> str:
        return self.question
     

class Option(models.Model):
    poll = models.ForeignKey("polls.Poll", verbose_name=_("Option Poll"), on_delete=models.CASCADE)
    option = models.CharField(_("Option"), max_length=255)

    def __str__(self) -> str:
        return f"{self.option} on poll {self.poll}"
    
    def get_absolute_url(self):
        return reverse("Option_detail", kwargs={"pk": self.pk})
    

class Vote(models.Model):
    author = models.ForeignKey(User, verbose_name=_("Vote Author"), on_delete=models.CASCADE)
    poll = models.ForeignKey("polls.Poll", verbose_name=_("Poll"), on_delete=models.CASCADE)
    option = models.ForeignKey("polls.Option", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Poll option vote")
        verbose_name_plural = ("Poll option votes")
    
    def __str__(self) -> str:
        return f"{self.author} voted {self.option[:30]} on {self.poll[:50]}"
    
    def get_absolute_url(self):
        return reverse("Poll_detail", kwargs={"pk": self.pk})
    

class Comment(models.Model):

    poll = models.ForeignKey("polls.Poll", verbose_name=_("Poll"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("Poll Author"), on_delete=models.CASCADE)
    content = models.TextField(_("Poll Comment"), max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"{self.content[:50]}"

    def get_absolute_url(self):
        return reverse("Comment_detail", kwargs={"pk": self.pk})

