from django.shortcuts import render
from django.views import generic

class UserProfile(generic.DetailView):
    template_name = "profile.html"