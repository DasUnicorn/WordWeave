from django.shortcuts import render
from django.views import generic
from .models import User

class UserProfileView(generic.DetailView):
    model = User
    template_name = "profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "user"