"""Query database and render HTML pages."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Article, ArticleCategory, Comment
from .forms import ArticleForm, CommentForm


def articles_list(request):
    """Query list of articles and render it as an HTML page."""
    user_is_authenticated = request.user.is_authenticated
    if user_is_authenticated:
        user_articles = Article.objects.filter(author=request.user)
    else:
        user_articles = []

    categories = ArticleCategory.objects.all()
    articles_categorized = []
    for category in categories:
        if user_is_authenticated:
            articles = Article.objects.filter(category=category).exclude(
                author=request.user
            )
        else:
            articles = Article.objects.filter(category=category)
        articles_categorized.append({
            'category_name': category.name,
            'category_description': category.description,
            'articles': articles,
        })

    ctx = {
        'user_articles': user_articles,
        'articles_categorized': articles_categorized,
    }

    return render(request, 'wiki/articles_list.html', ctx)


def article_detail(request, id):
    """Query article details and render it as an HTML page."""
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect(request.get_full_path())
    else:
        user_is_authenticated = request.user.is_authenticated
        user_is_author = request.user == article.author
        related_articles = Article.objects.filter(
            category=article.category
        ).exclude(id=article.id)[:3]
        comment_form = CommentForm()
        comments = Comment.objects.filter(article__id=id).order_by(
            '-created_on'
        )
        ctx = {
            'article': article,
            'related_articles': related_articles,
            'comments': comments,
            'comment_form': comment_form,
            'user_is_authenticated': user_is_authenticated,
            'user_is_author': user_is_author,
        }
    return render(request, 'wiki/article_detail.html', ctx)


@login_required
def article_create(request):
    """Create a new article and render the creation page."""
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect(article.get_absolute_url())
    else:
        article_form = ArticleForm()

    ctx = {
        'article_form': article_form,
    }
    return render(request, 'wiki/article_create.html', ctx)


@login_required
def article_update(request, id):
    """Update an existing article and render the update page."""
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        article_form = ArticleForm(
            request.POST, request.FILES, instance=article
        )
        if article_form.is_valid():
            article_form.save()
            return redirect(article.get_absolute_url())
    else:
        article_form = ArticleForm(instance=article)

    ctx = {
        'article_form': article_form,
    }
    return render(request, 'wiki/article_update.html', ctx)
