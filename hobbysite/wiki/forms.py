# app/forms.py
from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'entry']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']
        labels = {
            'entry': ''
        }
        widgets = {
            'entry': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your comment here...',
            }),
        }
