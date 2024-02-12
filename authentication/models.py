from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.CharField(max_length=200, unique=False, default="Your bio could be here.")
    created_on = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(null=True, blank=True, default="default.png", upload_to='assets')
