from django.shortcuts import redirect
from django.contrib import messages
from django.views import generic
from .models import Follower
from taggit.models import Tag
from django.contrib.auth.decorators import login_required


@login_required
def follow_tag(request):
    """
    Add follow relation between a logged in user and given tag.
    Throws warning message if user is already following the tag.
    """
    if request.method == 'POST':
        tag_name = request.POST.get('tag_name')
        if tag_name and request.user.is_authenticated:
            try:
                # Attempt to retrieve the tag from the database
                tag_to_follow = Tag.objects.get(name=tag_name)
                # Check if the user is already following the tag
                if Follower.objects.filter(followed_by=request.user,
                                           following=tag_to_follow).exists():
                    messages.warning(request, 'You are already following'
                                     f'{tag_to_follow.name}.')
                else:
                    Follower.objects.create(
                        followed_by=request.user, following=tag_to_follow)
                    messages.success(request, 'You are now following'
                                     f'{tag_to_follow.name}.')
                return redirect('tag_site', slug=tag_to_follow.slug)
            except Tag.DoesNotExist:
                # If the tag does not exist, redirect to the home page
                messages.error(request, 'Invalid tag name.')
                return redirect('home')
        else:
            messages.error(request, 'Invalid tag name.')
    return redirect('home')  # Redirect to home if user is not authenticated


@login_required
def unfollow_tag(request):
    """
    Remove follow relation between a logged in user and given tag.
    Throws warning message if user is not following the tag.
    """
    if request.method == 'POST':
        tag_name = request.POST.get('tag_name')
        if tag_name and request.user.is_authenticated:
            try:
                tag = Tag.objects.get(name=tag_name)
                if Follower.objects.filter(followed_by=request.user,
                                           following=tag).exists():
                    Follower.objects.filter(
                        followed_by=request.user, following=tag).delete()
                    messages.success(request, 'You have unfollowed'
                                     f'{tag.name}.')
                else:
                    messages.warning(request, 'You are not following'
                                     f'{tag.name}.')
                return redirect('tag_site', slug=tag.slug)
            except Tag.DoesNotExist:
                messages.error(request, 'Invalid tag name.')
        else:
            messages.error(
                request, 'Invalid tag name or user not authenticated.')
    # Redirect to home if tag is invalid or user is not authenticated
    return redirect('home')


class UserTagView(generic.ListView):
    """
    View displaying all tags a user is following.
    """
    template_name = "tag_user.html"
    context_object_name = 'followed_tags'

    def get_queryset(self):
        """Returns all Tags the logged in user follows."""
        user = self.request.user
        return Tag.objects.filter(following__followed_by=user)
