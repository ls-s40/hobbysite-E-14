"""Query database and render html page."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Article, ArticleCategory


def articles_list(request):
    """Query list of articles and render it as html page."""
    a = Article.objects.all().order_by('-created_on')
    ctx = {
        'articles': a
    }
    return render(request, 'wiki/articles_list.html', ctx)


def article_detail(request, id):
    """Query article details and render it as html page."""
    a = Article.objects.get(id=id)
    ctx = {
        'article': a
    }

    return render(request, 'wiki/article_detail.html', ctx)

def article_create(request):
    """Query article details and render it as html page."""

    articleCategories = ArticleCategory.objects.all()
    ctx = {
        'articleCategories': articleCategories
    }

    return render(request, 'wiki/article_create.html', ctx)

