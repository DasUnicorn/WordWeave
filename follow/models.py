from django.db import models
from django.conf import settings
from taggit.models import Tag

# Create your models here.

class Follower(models.Model):
	followed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_by")
	following = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="following")

	def __str__(self):
		return f"{self.followed_by.username} is following {self.following.name}"

	class Meta:
		unique_together = ('followed_by', 'following')
