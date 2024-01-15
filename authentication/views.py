from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormView
from .models import User
from .forms import ProfileUpdateForm
from django.urls import reverse_lazy 


class UserProfileView(generic.DetailView):
    model = User
    template_name = "profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "user"


class ProfileUpdateView(FormView):
    template_name = "update_profile.html"
    form_class = ProfileUpdateForm
    edit_only = True

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        current_user_profile = self.request.user
        
        current_user_profile.bio = form.instance.bio
        current_user_profile.profile_pic = form.instance.profile_pic
        current_user_profile.save()

        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("user_profile", args=[self.request.user.username]) 


