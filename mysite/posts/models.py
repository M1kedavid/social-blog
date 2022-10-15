from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

import misaka

from groups.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts',
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, default='This is a post!')
    message = models.TextField(default='')
    message_html = models.TextField(editable=False, default='')
    likes = models.ManyToManyField(
        User, blank=True, related_name="collected_votes")
    group = models.ForeignKey(
        Group, related_name='posts', null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("posts:single", kwargs={"username": self.user.username, 'pk': self.pk})

    class Meta:
        ordering = ['-created_at']
