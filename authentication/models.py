from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    bio = models.CharField(max_length=200, null=True, blank=True, unique=False,
                           default="Your bio could be here.")
    created_on = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(null=True, blank=True,
                                    upload_to='profiles')
