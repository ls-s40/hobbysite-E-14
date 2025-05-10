"""Query database and render html page."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Article, ArticleCategory
from .forms import ArticleForm


def articles_list(request):
    """Query list of articles and render it as html page."""
    a = Article.objects.all()
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
    if request.method == 'POST':
        articleForm = ArticleForm(request.POST)
        if articleForm.is_valid():
            article = articleForm.save(commit=False)
            article.author = request.user
            article.save()
            return redirect(article.get_absolute_url())
    else:
        articleForm = ArticleForm()
        ctx = {
            'articleForm' : articleForm
        }
        return render(request, 'wiki/article_create.html', ctx)

