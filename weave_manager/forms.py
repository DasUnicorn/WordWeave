from django import forms
from .models import Thread
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create Thread'))