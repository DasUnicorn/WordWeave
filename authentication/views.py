from django.shortcuts import render
from django.views import generic
from .models import Profile

class UserProfile(generic.ListView, user):
    queryset = Profile.objects.filter(user=user)
    template_name = "profile.html"