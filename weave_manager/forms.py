from django import forms
from .models import Thread, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content', 'picture', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # Check if Thread is created (has a primary key) and therefore will be edited
        # Or needs to be created.
        if self.instance and self.instance.pk:
            self.helper.add_input(Submit('submit', 'Edit Thread'))
        else:
            self.helper.add_input(Submit('submit', 'Create Thread'))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Comment'))
