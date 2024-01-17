from allauth.account.forms import SignupForm
from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from image_uploader_widget.widgets import ImageUploaderWidget
from crispy_forms.layout import Layout, Submit

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('bio', 'profile_pic')

    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_pic = forms.ImageField(widget=ImageUploaderWidget())

    def __init__(self, *args, **kwargs):
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
