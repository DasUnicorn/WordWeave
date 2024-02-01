from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .models import Follower
from taggit.models import Tag
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def follow_tag(request):
    if request.method == 'POST':
        tag_name = request.POST.get('tag_name')

        if tag_name and request.user.is_authenticated:
            tag_to_follow, created = Tag.objects.get_or_create(name=tag_name)

            # Check if the user is already following the tag
            if Follower.objects.filter(followed_by=request.user, following=tag_to_follow).exists():
                messages.warning(request, f'You are already following {tag_to_follow.name}.')
            else:
                Follower.objects.create(followed_by=request.user, following=tag_to_follow)
                messages.success(request, f'You are now following {tag_to_follow.name}.')
        else:
            messages.error(request, 'Invalid tag name.')

    return redirect('tag_site', slug=tag_to_follow.slug)

def unfollow_tag(request):
    if request.method == 'POST':
        tag_name = request.POST.get('tag_name')
        print(f'Tag name from form: {tag_name}')

        if tag_name and request.user.is_authenticated:
            tag = get_object_or_404(Tag, name=tag_name)
            
            if Follower.objects.filter(followed_by=request.user, following=tag).exists():
                Follower.objects.filter(followed_by=request.user, following=tag).delete()
                messages.success(request, f'You have unfollowed {tag.name}.')
            else:
                messages.warning(request, f'You are not following {tag.name}.')
        else:
            messages.error(request, 'Invalid tag name or user not authenticated.')

    return redirect('tag_site', slug=tag.slug)