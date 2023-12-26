from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=200, unique=False)
    created_on = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(null=True, blank=True)


    def __str__(self):
        return f"Profile for user: {self.user}"