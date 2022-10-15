from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="profile_pics")

    def __str__(self):
        return str(self.user)
