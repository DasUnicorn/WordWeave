from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

STATUS = ((0, "Draft"), (1, "Published"))


class Thread(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    votes = models.IntegerField(default=0)
    tags = TaggableManager()

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"The title of this thread is {self.title}"

class Comment(models.Model):
    Thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    votes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"
