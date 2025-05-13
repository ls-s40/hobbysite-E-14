"""Creates the form objects to be used on the web app."""

from django import forms
from .models import Thread, Comment


class ThreadForm(forms.ModelForm):
    """Defines form to create threads."""

    class Meta:
        """Identifies model and attributes to be filled in form."""

        model = Thread
        fields = ['title', 'category', 'entry', 'image']


class CommentForm(forms.ModelForm):
    """Defines form to create comments."""

    class Meta:
        """Identifies model and attributes to be filled in form."""

        model = Comment
        fields = ['entry']
        widgets = {
            'entry': forms.Textarea(attrs={'rows': 3, 
                                           'placeholder': 'Write a comment...'})
        }
