"""Query database and render html page."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Article, ArticleCategory, Comment
from .forms import ArticleForm, CommentForm


def articles_list(request):
    """Query list of articles and render it as html page."""
    articles = Article.objects.all()
    ctx = {
        'articles': articles
    }
    return render(request, 'wiki/articles_list.html', ctx)


def article_detail(request, id):
    """Query article details and render it as html page."""

    article = Article.objects.get(id=id)
    if request.method == 'POST':
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect(request.get_full_path())
    else:
        userIsAuthenticated = request.user.is_authenticated
        userIsAuthor = request.user == article.author
        relatedArticles = Article.objects.filter(category=article.category).exclude(id=article.id)[:3]
        commentForm = CommentForm()
        comments = Comment.objects.filter(article__id=id)
        ctx = {
            'article': article,
            'relatedArticles': relatedArticles,
            'comments': comments,
            'commentForm': commentForm,
            'userIsAuthenticated': userIsAuthenticated,
            'userIsAuthor': userIsAuthor
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

