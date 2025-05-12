"""This module contains form definitions for the wiki application."""

from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    """A form for creating and updating Article instances."""

    class Meta:
        """Meta options for the ArticleForm."""

        model = Article
        fields = ['title', 'category', 'entry', 'header_image']


class CommentForm(forms.ModelForm):
    """A form for creating and updating Comment instances."""

    class Meta:
        """Meta options for the CommentForm."""

        model = Comment
        fields = ['entry']
        labels = {
            'entry': '',
        }
        widgets = {
            'entry': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Write your comment here...',
                }
            ),
        }
