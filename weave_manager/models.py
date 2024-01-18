from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.conf import settings
from django.utils.text import slugify

STATUS = ((0, "Draft"), (1, "Published"))


class Thread(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    votes = models.IntegerField(default=0)
    tags = TaggableManager()

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"The title of this thread is {self.title}"

    # Creating the slug
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    votes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"
