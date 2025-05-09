# app/forms.py
from django import forms
from .models import Article, ArticleCategory

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'entry']
