from django.shortcuts import render
from django.views import generic
from .models import Profile

class UserProfile(generic.ListView):
    template_name = "profile.html"
    context_object_name = 'profiles'

    def get_queryset(self):
        username = self.kwargs['username']
        return Profile.objects.filter(user__username=username)