from allauth.account.forms import SignupForm
from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class CustomSignupForm(SignupForm):
    """
    Custom form for User Sign ups.
    Usernames can't be longer than 25 characters.
    """
    username = forms.CharField(max_length=25, label="Username")

    def clean_username(self):
        """Cleans username data."""
        username = self.cleaned_data['username']
        return username


class ProfileUpdateForm(forms.ModelForm):
    """
    Form to update bio and profile pic of User.
    """
    class Meta:
        """Setting DB to User and fields to bio and pic"""
        model = User
        fields = ('bio', 'profile_pic')

    bio = forms.CharField(required=False,
                          widget=forms.TextInput(
                           attrs={'class': 'form-control'}))
    profile_pic = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        """Initialize ProfileUpdateForm"""
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'bio',
            'profile_pic',
            Submit('submit', 'Update Profile')
        )

        # Set initial values based on the existing user profile data
        current_user = self.instance
        if current_user:
            self.initial['bio'] = current_user.bio
            self.initial['profile_pic'] = current_user.profile_pic
