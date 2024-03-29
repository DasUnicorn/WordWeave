from django.views import generic
from django.views.generic.edit import FormView
from .models import User
from weave_manager.models import Thread, Comment
from django.db.models import Sum
from .forms import ProfileUpdateForm
from django import forms
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin


class UserProfileView(generic.DetailView):
    """
    This View displays the User Profile.
    """
    model = User
    template_name = "profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        """Get context data to display in the template"""
        context = super().get_context_data(**kwargs)

        # Calculate the sum of votes for all threads by the user
        user_threads = Thread.objects.filter(author=self.object)
        thread_votes = user_threads.aggregate(Sum('votes'))['votes__sum']
        if not thread_votes:
            thread_votes = 0

        # Calculate the sum of votes for all comments by the user
        user_comments = Comment.objects.filter(author=self.object)
        comment_votes = user_comments.aggregate(Sum('votes'))['votes__sum']
        if not comment_votes:
            comment_votes = 0

        # Add all votes for total sum
        total_votes = thread_votes + comment_votes

        context['total_votes'] = total_votes

        return context


class ProfileUpdateView(LoginRequiredMixin, FormView):
    """
    View to Update the Profile User Data.
    User need to be logged in.
    """
    template_name = "update_profile.html"
    form_class = ProfileUpdateForm
    edit_only = True

    class Meta:
        """Set User model, bio and pic field"""
        model = User
        fields = ('bio', 'profile_pic')

    bio = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    profile_pic = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}))

    def get_form_kwargs(self):
        """Get keyword arguments"""
        kwargs = super().get_form_kwargs()
        # Set the instance to the current user's profile
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Validate the ProfileUpdateForm."""
        current_user_profile = self.request.user
        current_user_profile.bio = form.cleaned_data['bio']

        if form.cleaned_data['profile_pic']:
            current_user_profile.profile_pic = form.cleaned_data['profile_pic']
        else:
            # Cloudfare bucket returns False when clearing images.
            # Since False can't be written into the ImageField
            # we have to set it to None.
            current_user_profile.profile_pic = None
        current_user_profile.save()

        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        """
        Return the succes url.

        Arguments:
        username -- the username of the profile as parameter name
        """
        return reverse_lazy("user_profile", args=[self.request.user.username])


@login_required
def delete_profile(request, user_id):
    """
    Delete given User.
    User must be logged in.

    Keyword Arguments:
    user_id -- the id of the user you want to delete
    """
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST' and request.user == user:
        user.delete()
        return redirect('home')

    # Render the delete confirmation page
    return render(request, 'delete_profile_confirm.html', {'user': user})
