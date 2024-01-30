from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormView
from .models import User
from .forms import ProfileUpdateForm
from django import forms
from django.urls import reverse_lazy
from image_uploader_widget.widgets import ImageUploaderWidget
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, reverse


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

    class Meta:
        model = User
        fields = ('bio', 'profile_pic')

    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_pic = forms.ImageField(widget=ImageUploaderWidget())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Set the instance to the current user's profile
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):

        print(f"Authenticated User: {self.request.user}")

        current_user_profile = self.request.user
        current_user_profile.bio = form.cleaned_data['bio']
        current_user_profile.profile_pic = form.cleaned_data['profile_pic']
        current_user_profile.save()

        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        # Use 'username' as the parameter name
        return reverse_lazy("user_profile", args=[self.request.user.username])

@login_required
def delete_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST' and request.user == user:
        user.delete()
        return redirect('home')

    return redirect('profile', user.username)

