"""Query database and render html page."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Article, ArticleCategory, Comment
from .forms import ArticleForm, CommentForm


def articles_list(request):
    """Query list of articles and render it as html page."""

    user_is_authenticated = request.user.is_authenticated
    if user_is_authenticated:
        user_articles = Article.objects.filter(author=request.user)
    else:
        user_articles = []
    categories = ArticleCategory.objects.all()
    articles_categorized = []
    for category in categories:
        if user_is_authenticated:
            articles = Article.objects.filter(category = category).exclude(author=request.user)
        else:
            articles = Article.objects.filter(category = category)
        articles_categorized.append({ 
            'category_name': category.name,
            'category_description': category.description,
            'articles': articles
        })
    
    ctx = {
        'user_articles': user_articles,
        'articles_categorized': articles_categorized
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

@login_required
def article_create(request):
    """Query article details and render it as html page."""
    if request.method == 'POST':
        articleForm = ArticleForm(request.POST, request.FILES)
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

@login_required
def article_update(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        articleForm = ArticleForm(request.POST, request.FILES, instance=article)
        if articleForm.is_valid():
            articleForm.save()
            return redirect(article.get_absolute_url())
    else:
        articleForm = ArticleForm(instance=article)
        ctx = {
            'articleForm': articleForm
        }

    return render(request, 'wiki/article_update.html', ctx)
