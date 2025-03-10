"""This file contains the views for the blog app."""
from django.shortcuts import render, get_object_or_404
from .models import Article, ArticleCategory


def article_list(request):
    """Display a list of articles."""
    categories = ArticleCategory.objects.all()
    return render(request, 'article_list.html', {'categories': categories})


def article_detail(request, id):
    """Display a single article."""
    article = get_object_or_404(Article, id=id)
    return render(request, 'article_detail.html', {'article': article})
