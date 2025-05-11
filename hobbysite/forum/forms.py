"""Creates the form objects to be used on the web app."""

from django import forms
from .models import Thread

class ThreadForm(forms.ModelForm):
    """Defines form to create threads."""

    class Meta:
        """Identifies model and attributes to be filled in form."""

        model = Thread
        fields = ['title', 'category', 'entry', 'image']