from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """Form for adding comments to articles."""
    class Meta:
        model = Comment
        fields = ['entry']