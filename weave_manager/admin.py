from django.contrib import admin
from .models import Thread, Comment, CommentVote, ThreadVote

# Register your models here.
admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(CommentVote)
admin.site.register(ThreadVote)
