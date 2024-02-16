from allauth.account.forms import SignupForm
from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from image_uploader_widget.widgets import ImageUploaderWidget
from crispy_forms.layout import Layout, Submit

class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=25, label="Username")

    def clean_username(self):
        username = self.cleaned_data['username']
        return username

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('bio', 'profile_pic')

    bio = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_pic = forms.ImageField(required=False)

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

    def form_valid(self, form):
        # Save the form data
        self.object = form.save(commit=False)
        
        # Check if the user wants to clear the profile picture
        if form.cleaned_data['clear_profile_pic']:
            self.object.profile_pic = None

        self.object.save()
        return super().form_valid(form)
