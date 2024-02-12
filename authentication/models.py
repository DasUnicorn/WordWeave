from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.CharField(max_length=200, unique=False, default="Your bio could be here.")
    created_on = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(null=True, blank=True, default="default.png", upload_to='profiles')

    def save(self, *args, **kwargs):
        # Check if the instance has a primary key (i.e., if it's an existing user)
        if self.pk:
            try:
                current_user = User.objects.get(pk=self.pk)
                # If the profile picture exist and has changed, delete the old one
                if current_user.profile_pic and self.profile_pic != current_user.profile_pic:
                    # Delete the old profile picture from storage bucket
                    if os.path.isfile(current_user.profile_pic.path):
                        os.remove(current_user.profile_pic.path)
            except User.DoesNotExist:
                raise ValueError("User does not exist")
        # Save the new profile picture
        super().save(*args, **kwargs)

