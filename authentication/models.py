from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist

class User(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    bio = models.CharField(max_length=200, null=True, blank=True, unique=False, default="Your bio could be here.")
    created_on = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profiles')

    def save(self, *args, **kwargs):
        # Check if the instance has a primary key
        if self.pk:
            try:
                current_user = User.objects.get(pk=self.pk)
                # If the profile picture exist and has changed, delete the old one
                if current_user.profile_pic and self.profile_pic != current_user.profile_pic:
                    # Delete the old profile picture from the Cloudflare R2 bucket
                    try:
                        default_storage.delete(current_user.profile_pic.name)
                        self.profile_pic.delete(save=False) 
                    except FileNotFoundError:
                        pass  # If the file does not exist, do nothing
            except ObjectDoesNotExist:
                raise ValueError("User does not exist")
        super().save(*args, **kwargs)

