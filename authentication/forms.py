from allauth.account.forms import SignupForm
from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from image_uploader_widget.widgets import ImageUploaderWidget

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

        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': ImageUploaderWidget(attrs={'accept': 'image/png'}),
        }
