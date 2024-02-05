from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_delete
from django.dispatch import receiver

STATUS = ((0, "Draft"), (1, "Published"))

class Thread(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    votes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
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

    def up_vote(self, user):
        # Check if the user has already voted for the thread
        if not self.thread_votes.filter(user=user).exists():
            self.votes = F('votes') + 1
            self.save()
            self.thread_votes.create(user=user, value=1)
        elif self.thread_votes.get(user=user, thread_id=self.id).value == -1:
            self.votes = F('votes') + 2
            self.save()
            vote = self.thread_votes.get(user=user, thread_id=self.id)
            vote.value = 1
            vote.save()
        # Here need to come an exception that gets handle to inform the user that they have already voted.

    def down_vote(self, user):
        # Check if the user has already voted for the thread
        if not self.thread_votes.filter(user=user).exists():
            self.votes = F('votes') - 1
            self.save()
            self.thread_votes.create(user=user, value=-1)
        elif self.thread_votes.get(user=user, thread_id=self.id).value == 1:
            self.votes = F('votes') - 2
            self.save()
            vote = self.thread_votes.get(user=user, thread_id=self.id)
            vote.value = -1
            vote.save()
        # Here need to come an exception that gets handle to inform the user that they have already voted.

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

    def up_vote(self, user):
        # Check if the user has already voted for the thread
        if not self.comment_votes.filter(user=user).exists():
            self.votes = F('votes') + 1
            self.save()
            self.comment_votes.create(user=user, value=1)
        elif self.comment_votes.get(user=user, comment_id=self.id).value == -1:
            self.votes = F('votes') + 2
            self.save()
            vote = self.comment_votes.get(user=user, comment_id=self.id)
            vote.value = 1
            vote.save()
        # Here need to come an exception that gets handle to inform the user that they have already voted.

    def down_vote(self, user):
        # Check if the user has already voted for the thread
        if not self.comment_votes.filter(user=user).exists():
            self.votes = F('votes') - 1
            self.save()
            self.comment_votes.create(user=user, value=-1)
        elif self.comment_votes.get(user=user, comment_id=self.id).value == 1:
            self.votes = F('votes') - 2
            self.save()
            vote = self.comment_votes.get(user=user, comment_id=self.id)
            vote.value = -1
            vote.save()
        # Here need to come an exception that gets handle to inform the user that they have already voted.


class ThreadVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    value = models.SmallIntegerField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="thread_votes")

class CommentVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    value = models.SmallIntegerField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment_votes")


@receiver(pre_delete, sender=ThreadVote)
def update_thread_votes(sender, instance, **kwargs):
    if instance.value == 1:
        instance.thread.votes = F('votes') - 1
    elif instance.value == -1:
        instance.thread.votes = F('votes') + 1
    instance.thread.save()

@receiver(pre_delete, sender=CommentVote)
def update_comment_votes(sender, instance, **kwargs):
    if instance.value == 1:
        instance.comment.votes = F('votes') - 1
    elif instance.value == -1:
        instance.comment.votes = F('votes') + 1
    instance.comment.save()